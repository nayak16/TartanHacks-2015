function resizeContent() {
    $height = $(window).height()-48;
    $('body .banner').height($height);
}

$(document).ready(function(){
    resizeContent();

    $(window).resize(function() {
        resizeContent();
    });

    $('a[href^="#"]').on('click',function (e) {
	    e.preventDefault();

	    var target = this.hash;
	    var $target = $(target);

	    $('html, body').stop().animate({
	        'scrollTop': $target.offset().top
	    }, 900, 'swing', function () {
	        window.location.hash = target;
	    });
	});
});