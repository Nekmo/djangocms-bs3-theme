from django.template.base import token_kwargs
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template
from django.template.loader_tags import ExtendsNode, register, IncludeNode
from django.template import TemplateSyntaxError
from django.utils.safestring import SafeText

from cms_bs3_theme import conf


def template_to_theme(filter_expression, context):
    theme = context.get('bs3_conf', {}).get('BOOTSTRAP3_THEME', conf.BOOTSTRAP3_THEME)
    app, path = filter_expression.var.split('/', 1)
    template_theme = '{0}/themes/{1}/{2}'.format(app, theme, path)
    try:
        get_template(template_theme)
    except TemplateDoesNotExist:
        pass
    else:
        filter_expression.token = repr(template_theme)
        filter_expression.var = SafeText(template_theme)
    return filter_expression


class Bs3ExtendsNode(ExtendsNode):
    bs3_conf = None

    # def find_template(self, template_name, context):
    #     return super(Bs3ExtendsNode, self).find_template(template_name, context)

    def render(self, context):
        self.parent_name = template_to_theme(self.parent_name, context)
        print(self.parent_name)
        return super(Bs3ExtendsNode, self).render(context)


class Bs3IncludeNode(IncludeNode):
    context_key = '__include_context'

    def render(self, context):
        """
        Render the specified template and context. Cache the template object
        in render_context to avoid reparsing and loading when used in a for
        loop.
        """
        self.template = template_to_theme(self.template, context)
        return super(Bs3IncludeNode, self).render(context)


@register.tag
def bs3_extends(parser, token):
    """
    """
    bits = token.split_contents()
    if len(bits) != 2:
        raise TemplateSyntaxError("'%s' takes one argument" % bits[0])
    parent_name = parser.compile_filter(bits[1])
    nodelist = parser.parse()
    if nodelist.get_nodes_by_type(ExtendsNode):
        raise TemplateSyntaxError("'%s' cannot appear more than once in the same template" % bits[0])
    return Bs3ExtendsNode(nodelist, parent_name)


@register.tag('bs3_include')
def do_include(parser, token):
    """
    Loads a template and renders it with the current context. You can pass
    additional context using keyword arguments.

    Example::

        {% include "foo/some_include" %}
        {% include "foo/some_include" with bar="BAZZ!" baz="BING!" %}

    Use the ``only`` argument to exclude the current context when rendering
    the included template::

        {% include "foo/some_include" only %}
        {% include "foo/some_include" with bar="1" only %}
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError(
            "%r tag takes at least one argument: the name of the template to "
            "be included." % bits[0]
        )
    options = {}
    remaining_bits = bits[2:]
    while remaining_bits:
        option = remaining_bits.pop(0)
        if option in options:
            raise TemplateSyntaxError('The %r option was specified more '
                                      'than once.' % option)
        if option == 'with':
            value = token_kwargs(remaining_bits, parser, support_legacy=False)
            if not value:
                raise TemplateSyntaxError('"with" in %r tag needs at least '
                                          'one keyword argument.' % bits[0])
        elif option == 'only':
            value = True
        else:
            raise TemplateSyntaxError('Unknown argument for %r tag: %r.' %
                                      (bits[0], option))
        options[option] = value
    isolated_context = options.get('only', False)
    namemap = options.get('with', {})
    return Bs3IncludeNode(parser.compile_filter(bits[1]), extra_context=namemap,
                       isolated_context=isolated_context)
