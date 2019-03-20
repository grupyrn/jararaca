(function($){
  $(function(){

    $('.sidenav').sidenav().on('click tap', 'li a', () => {
      $('.sidenav').sidenav('close');
    });


    $('.parallax').parallax();
    $('.scrollspy').scrollSpy();

  }); // end of document ready
})(jQuery); // end of jQuery name space
