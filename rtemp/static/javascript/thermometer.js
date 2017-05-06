$(document).ready(function(){
  update_thermometer();
  $('#qr').qrcode("this plugin is great");
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
     }
     });
  });

  function update_thermometer() {
    var status_url = $("#fluid").attr('data-status');
    $.ajax({
      url: status_url,
      dataType: 'json',
      success: function (data) {
        $("#fluid").animate({
          'height': data.percent+"%"},800,"swing"
        );
        $("#attendee_count").text(data.attendees);
        $("#vote_count").text(data.percent)
        if (data.able_to_vote == false){
          $("#vote").addClass('disabled');
        }else{
          $("#vote").removeClass('disabled');
        }
      }
    })
    return true;              // The function returns the product of p1 and p2
  }

});
