(function($){
  $(function(){

    $('.sidenav').sidenav();

  }); // end of document ready
})(jQuery); // end of jQuery name space
$(document).ready(function () {
  $('.tooltipped').tooltip();
});
$(".card-content").click(function () {
  $('.modal').modal();
});