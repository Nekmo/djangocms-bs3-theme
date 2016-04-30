process.chdir('cms_bs3_theme/static/cms_bs3_theme');
var gulp = require('gulp'),
    compass = require('gulp-compass');
    cleanCSS = require('gulp-clean-css');


// Fonts
gulp.task('fonts-fontawesome', function() {
    return gulp.src([
        'src/libs/font-awesome/fonts/fontawesome-webfont*'])
        .pipe(gulp.dest('dist/fonts/font-awesome'));
});
gulp.task('fonts-glyphicons', function() {
    return gulp.src([
        'src/libs/bootstrap-sass/assets/fonts/bootstrap/glyphicons-*'])
        .pipe(gulp.dest('dist/fonts/bootstrap'));
});
gulp.task('copy-fonts', ['fonts-glyphicons', 'fonts-fontawesome']);


// CSS
gulp.task('sass', function () {
    return gulp.src(['src/scss/*.scss'])
        .pipe(compass({
            css: 'dist/css',
            sass: 'src/scss',
            environment: 'production'
        }))
});
gulp.task('minify-css', ['sass'], function() {
    return gulp.src(['dist/css/*.css'])
        .pipe(cleanCSS())
        .pipe(gulp.dest('dist/css/'));
});


gulp.task('default', function() {
    // place code for your default task here
    gulp.start('minify-css', 'copy-fonts');
});