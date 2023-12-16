// Parallax effect where the part of the page with the class parallaxImage scroll slower than the rest.

var initialScroll = window.pageYOffset;

window.addEventListener('scroll', function() {
    var parallaxImages = document.getElementsByClassName('parallaxImage');

    var pixel_scrolled = -(window.pageYOffset * 0.1); // Adjust '0.5' for speed

    for (let i = 0; i < parallaxImages.length; i++) {

        var computedStyle = window.getComputedStyle(parallaxImages[i]);
        var currentTransform = computedStyle.transform || computedStyle.webkitTransform;

        if (currentTransform.includes('matrix')) {
            var values = currentTransform.match(/matrix\(([^)]+)\)/)[1].split(', ').map(parseFloat);
            values[5] = pixel_scrolled;
            console.log(values[5])
            parallaxImages[i].style.transform = 'matrix(' + values.join(', ') + ')';
        } else {
            parallaxImages[i].style.transform = 'matrix(0,0,0,0,0,0)';
        }
    }
});
