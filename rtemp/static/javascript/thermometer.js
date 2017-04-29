$(document).ready(function(){

  $("#vote").click(function(){
   button = $(this)
   var room = button.attr('data-url');
   $.ajax({
     url: room,
     dataType: 'json',
     success: function (data) {
       button.addClass('disabled');
       setTimeout(function() {
         button.removeClass('disabled');
       }, data.interval*1000);
     }
     });
  });
});
