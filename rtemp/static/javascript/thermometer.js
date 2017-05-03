$(document).ready(function(){
  update_thermometer();
  var update_interval = setInterval(update_thermometer, 15000);

  $("#vote").click(function(){
   button = $(this)
   var room_url = button.attr('data-url');
   var status_url = $("#fluid").attr('data-status');
   $.ajax({
     url: room_url,
     dataType: 'json',
     success: function (data) {
       update_thermometer();
       button.addClass('disabled');
       setTimeout(function() {
         button.removeClass('disabled');
       }, data.interval*1000);
     }
     });
  });

  function update_thermometer() {
    var status_url = $("#fluid").attr('data-status');
    $.ajax({

      url: status_url,
      dataType: 'json',
      success: function (data) {

        $("#fluid").css('height', data.percent+"%");
      }
    })
    return true;              // The function returns the product of p1 and p2
  }

});
