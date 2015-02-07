function resizeContent() {
    $height = $(window).height();
    $('body .banner').height($height-48);
    $('body .more_info').height($height);
    $('body .banner_overlay').css("top",($height/4));
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

	$('#scroll_to').on('click',function(){
		console.log("here");
	});
});