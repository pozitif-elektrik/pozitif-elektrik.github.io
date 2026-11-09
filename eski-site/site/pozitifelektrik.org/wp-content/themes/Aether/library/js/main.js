function adjustHomePage(){
    var windowHeight = jQuery(this).height();
    if( windowHeight < 600 ){ windowHeight = 600; }
    jQuery('#home').height(windowHeight + 1);
}


jQuery(window).on('resize', function($){
    adjustHomePage();
    setTimeout( function(){
        jQuery('body').removeAttr('style');
    }, 500);
});

/*=====================
   Automatic skroll data animation
  =====================*/
jQuery(window).load(function($){
    // Resize Home Page
    adjustHomePage();


    if( ! /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) && parallax != -1){
        skrollr.init({
            forceHeight: false
        });
    }

    //$('body').removeAttr('style');
});

var menuFixed = 0;
jQuery(window).scroll(function($){

    if( jQuery(window).scrollTop() > jQuery(window).height() && menuFixed === 0 ){
        jQuery('#main-nav').css({'position': 'fixed', 'top': '-100px'});
        jQuery('#main-nav').animate({
            top: 0
        }, 500);

        jQuery('#scrollToTop').fadeTo(300, 0.5);
        menuFixed = 1;

        if( jQuery('#bg_video').length > 0 ){
            document.getElementById('bg_video').pause();
        }
    }

    if( jQuery(window).scrollTop() < jQuery(window).height() && menuFixed == 1){
        jQuery('#main-nav').animate({
            top: '-100px'
        }, 200, function(){
            jQuery(this).removeAttr('style');
        });
        jQuery('#scrollToTop').fadeOut(600);
        menuFixed = 0;

        if( jQuery('#bg_video').length > 0 ){
            document.getElementById('bg_video').play();
        }
    }

});


jQuery(document).ready(function($){

    if( ! /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)  && $('#home').length > 0){
        $("body").queryLoader2({
            barColor: "#333",
            backgroundColor: "#fff",
            percentage: true,
            barHeight: 3,
            completeAnimation: "grow",
            minimumTime: 100
        });
    }

    $( "#blog-post article iframe" ).each(function(index, value){

        var eWidth = parseInt($(value).attr('width')),
            eHeight;

        if($(value).attr('width').indexOf('%') > -1){
            // percent
            eHeight = eWidth / 1.7777 + '%';
            eWidth = eWidth + '%';
        }else{
            //px
            eHeight = eWidth / 1.7777 + 'px';
            eWidth = eWidth + 'px';
        }

        $(value).wrap( "<div class='video-container' style='width: " + eWidth + "; padding-bottom:" + eHeight + ";'></div>" );
    });


    $('.dropdown-menu-placeholder').on('click', function(e){
        e.preventDefault();

        if( ! $(this).siblings('nav').is(":visible")){
            $(this).siblings('nav').slideDown();
        }else{
            $(this).siblings('nav').slideUp();
        }
    });

    if( $('#home #slide-show .img').length > 1 ){
        setInterval(function(){
            var visibleSlide = $('#home #slide-show .img').last();
            visibleSlide.prev().fadeIn(1000);
            visibleSlide.fadeOut(1000, function(){
                var temp = $(this).detach();
                $('#home #slide-show').prepend(temp);
            });
        }, 3000);
    }

/*=====================
   Home page Animation
  =====================*/
	var startButton = {
        container: "#start-button",
        isPulsing: false,
        init: function(){
            var _self = this;
            var initialMargin = $(_self.container).find('img').css('margin-top');
            $(_self.container).on('mouseenter', function(){
                $(this).find('img').stop(true,true).animate({
                    'margin-top': '0',
                    'opacity'   : '1'
                }, function(){
                    _self.pulse();
                });
            });
            $(_self.container).on('mouseleave', function(){
                $(this).find('img').stop(true,true).animate({
                    'margin-top': initialMargin,
                    'opacity'   : '0'
                });
                $(_self.container).find('.glow').stop(true,true).hide();
                clearTimeout(_self.isPulsing);
            });
            $(_self.container).on('click', function(e){
                e.preventDefault();

                $('html, body').animate({
                    scrollTop: $(_self.container).parents('#home').outerHeight()
                }, 800);
            });
        },
        pulse: function(){
            var _self = this;
            _self.isPulsing = setTimeout(function(){
                $(_self.container).find('.glow').fadeIn(600, function(){
                    $(this).fadeOut(600);
                });
                _self.pulse();
            });
        }
	};
/*=====================
   Portfolio page Animation
  =====================*/
var portfolio = {
    mainContainer: '#portfolio',
    postsContainer: '#recent-projects .posts',
    detailsContainer: '.project-details',
    currentRow: '',
    allProjects: null,
    filtering: false,

    init: function(){
        var _self = this;
        _self.allProjects = $(_self.postsContainer).find('figure');

        //bindings
        $( _self.postsContainer).on('click', 'figure', function(){
            $('<div class="loading-portfolio">Loading ...</div>').appendTo('body');
            var clickedElem = $(this);
            _self.loadContent(clickedElem);
        });

        $('body').on('click',  _self.detailsContainer + ' .close-button', function(e){
            e.preventDefault();
            _self.hide( function(){});
        });

        $('#portfolio-filter a').on('click', function(e){
            e.preventDefault();
            _self.hide();

            if(!_self.filtering){
                _self.filtering = true;
                $(this).closest('ul').find('a').removeClass('active');
                $(this).addClass('active');
                _self.filter($(this).data('filter'));
            }
        });



        //custom lightbox
        $(_self.mainContainer).on('click', _self.detailsContainer + ' figure > a', function(e){
            e.preventDefault();
            $(this).siblings('.md-modal').removeAttr('style');
            var emptySpace = $(window).height() - $(this).siblings('.md-modal').outerHeight(true);

            if(emptySpace >= 100 ){
                $('#lightbox').css({ 'margin-top' : emptySpace/2, 'margin-bottom' : emptySpace/2 });
            }else{
                $('#lightbox').css({ 'height' : $(window).height() - 100, 'margin-top' : '50px', 'margin-bottom' : '50px', 'width' : 'auto' });
                $('#lightbox').css({ 'width' : $('#lightbox .md-content img').width() });
            }

            $('#lightbox').addClass('md-show');
        });

        $(_self.detailsContainer).on('click','figure .md-overlay, figure .md-close', function(e){
            e.preventDefault();
            $(_self.detailsContainer).find('.md-modal').removeClass('md-show');
        });

    },

    loadContent: function(clickedElem){
        var _self = this;

        $.ajax({
            url: clickedElem.data('link'),
            type: 'get',
            cache: false,
            async: true,
            success: function(response){
                _self.show(clickedElem, response);
            }
        });
    },

    show: function(clickedElem, content){
        var _self = this;

        $('.loading-portfolio').fadeOut( function(){ $(this).remove(); });

        if( $('.project-details').is(':visible') ){
            if( clickedElem.parents('.posts').is(_self.currentRow) ){
                $('.project-details .container').fadeOut(function(){
                    $(this).remove();
                    $('.project-details').append(content).find('.container').css('display','none').fadeIn();
                });
            }else{
                _self.hide( function(){ _self.show(clickedElem, content); });
            }
        }else{

            $('.project-details .container').remove();
            $('#recent-projects .project-details').append(content);

            $('#recent-projects .project-details img.wp-post-image').on('load', function(){
                clickedElem.parents('.posts').animate({ 'margin-bottom' : $('.project-details').outerHeight(true)  });
                $('.project-details').css({ 'top' : clickedElem.position().top + clickedElem.height() }).slideDown(function(){
                    $('html, body').animate({scrollTop:$('#recent-projects .project-details').offset().top-100}, 'slow');
                });
            });

            _self.currentRow = clickedElem.parents('.posts');
        }
    },

    hide: function(callback){
        var _self = this;

        $('#recent-projects .posts').animate({ 'margin-bottom' : 0 });
        $('.project-details').slideUp( callback );
    },

    filter: function(label){
        var _self = this;
        var filteredProjects;

        if(label == "all"){
            filteredProjects = _self.allProjects;
        }else{
            filteredProjects = _self.allProjects.filter(function(index, value){
                var labelArray = $.trim( $(value).data('label') ).split(' ');
                if( $.inArray(label, labelArray) != -1 ){
                    return this;
                }
            });
        }

        console.log('test');


        $.when( $(_self.postsContainer).find('figure').stop(true,true).fadeOut(200) ).done(function() {
            $(_self.postsContainer).find('figure').remove();

            $.each(filteredProjects, function(index, value){

                // var total = $matches.length/2;
                if( index < filteredProjects.length/2 ){
                    $('#recent-projects .posts').eq(0).append( $(value) ).append('\n').find('figure').delay(300).stop(true,true).fadeIn(300, function(){ _self.filtering = false; });
                }else{
                    $('#recent-projects .posts').eq(1).append( $(value) ).append('\n').find('figure').delay(300).stop(true,true).fadeIn(300, function(){ _self.filtering = false; });
                }
            });

        });

        // setTimeout(function(){

        // }, 300);


    }

};


/*=====================
   Blog Page Animation
  =====================*/
var searchBlog = {
    container: '#blog',
    posts: '#recent-posts',
    input: '.special-section input[type="text"]',
    postObject: '',

    init: function(){
        var _self = this;
        var allPosts = $(_self.container + ' ' + _self.posts).find('figure');
        var timer;

        $('#blog form').submit(function(e){
            e.preventDefault();
        });


        $(_self.container).find(_self.input).change( function () {
            var filter = $(this).val();

            clearTimeout(timer);
            timer = setTimeout(function(){

                $matches = (filter.length > 0) ? allPosts.find('.post-title span:contains(' + filter + ')').closest('figure') : allPosts;
                $.when( $('#recent-posts .posts figure').fadeOut(300) ).done(function() {
                    $('#recent-posts .posts figure').remove();
                    _self.showPosts($matches);
                });

            }, 1000);


            return false;
        }).keyup( function () {  $(this).change(); });

    },
    showPosts: function($matches){

        // Show posts
        $.each($matches, function(index, value){

            // var total = $matches.length/2;
            if( index < $matches.length/2 ){
                $('#recent-posts .posts').eq(0).append( $(value) ).append('\n').find('figure').fadeIn(300);
            }else{
                $('#recent-posts .posts').eq(1).append( $(value) ).append('\n').find('figure').fadeIn(300);
            }
        });
    }
};


/*=====================
   Contact page Animation
  =====================*/
    $.get('//maps.googleapis.com/maps/api/geocode/json?address=' + contact_address + '&sensor=false', function(data){
        var location = data.results[0].geometry.location;


        function initialize(location) {
            var coordinates = new google.maps.LatLng(location.lat, location.lng);
            var mapOptions = {
                zoom: 14,
                center: coordinates,
                disableDefaultUI: true,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };

            var map = new google.maps.Map(document.getElementById('map-canvas'),mapOptions);
            new google.maps.Marker({
                position: coordinates,
                map: map,
                title: 'Contact Address'
            });

            map.panBy(0,-250);

        }

        if ( $('#map-canvas').length > 0 ){
            google.maps.event.addDomListener(window, 'load', initialize(location));
        }

    });


    $('#contact .button').on('click', function(e){
        e.preventDefault();

        var contactFrom = $('#contact form');
        var hideMessagesDelay;
        contactFrom.find('.form-messages').stop(true,true).slideUp(500);

        $.ajax({
            url: contactFrom.attr('action'),
            type: "POST",
            data: contactFrom.serialize(),
            dataType: 'json',
            cache: false,
            success: function(response) {
                contactFrom.find('.form-messages').html(response.message).slideDown(500);
                if(response.sent){
                    contactFrom.find('.form-messages').removeClass('error').addClass('success');
                    contactFrom[0].reset();
                }else{
                    contactFrom.find('.form-messages').removeClass('success').addClass('error');
                }

                clearTimeout(hideMessagesDelay);
                hideMessagesDelay = setTimeout(function(){
                    contactFrom.find('.form-messages').slideUp(500);
                }, 8000);
            }
        }); // end ajax

    });



/*=====================
   INITS
  =====================*/
    portfolio.init();
    searchBlog.init();
    startButton.init();


    $('.skill').waypoint(function(direction) {
        $('.skill span').each(function(index, value){
            $(value).css('width','0');
            $(value).animate({
                'width' : $(this).data('percent')
            },{
                duration: 1500,
                step: function(now){
                    $(this).text( Math.round(now) + "%");
                }
            });

        });

    }, { offset: 'bottom-in-view', triggerOnce: true });


/*=====================
   Menu
  =====================*/
    $(document).keydown(function(e){
        var currentMenuItem = $('#main-nav nav ul .current');
        if (e.keyCode == 38) {
            currentMenuItem.prev().find('a').trigger('click');
            e.preventDefault();
        }else if(e.keyCode == 40){
            currentMenuItem.next().find('a').trigger('click');
            e.preventDefault();
        }
    });

    $('#main-nav nav ul').onePageNav({
        scrollOffset: 62,
        scrollSpeed: 1400,
        filter: ':not(.exclude)',
        begin: function() {

        },
        end: function() {

        },
        scrollChange: function($currentListItem){

        }
    });


/*=====================
   Scroll To TOP
  =====================*/
    $('#scrollToTop').on('click', function(e){
        e.preventDefault();
        $('html,body').animate({ scrollTop: 0 }, 2000);
    });
});