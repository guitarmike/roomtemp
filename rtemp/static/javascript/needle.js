$(document).ready(function(){

  $('#qr').qrcode($("#main_container").data("page-url"));

  var opts = {
    angle: 0, // The span of the gauge arc
    lineWidth: 0.24, // The line thickness
    radiusScale: 1, // Relative radius
    pointer: {
      length: 0.46, // // Relative to gauge radius
      strokeWidth: 0.035, // The thickness
      color: '#000000' // Fill color
    },
    limitMax: false,     // If false, the max value of the gauge will be updated if value surpass max
    limitMin: true,     // If true, the min value of the gauge will be fixed unless you set it manually
    colorStart: '#6FADCF',   // Colors
    colorStop: '#8FC0DA',    // just experiment with them
    strokeColor: '#E0E0E0',  // to see which ones work best for you
    generateGradient: true,
    highDpiSupport: true,     // High resolution support
    staticZones: [
       {strokeStyle: "#F03E3E", min: 0, max: 50}, // Red from 100 to 130
       {strokeStyle: "#425ff4", min: 50, max: 100}
    ]
  };
  var target = document.getElementById('gauge'); // your canvas element
  var gauge = new Gauge(target).setOptions(opts); // create sexy gauge!
  gauge.maxValue = 100; // set max gauge value
  gauge.setMinValue(0);  // Prefer setter over gauge.minValue = 0
  gauge.animationSpeed = 5; // set animation speed (32 is default value)
  update_needle();

  var update_interval = setInterval(update_needle, 5000);

  $(".vote_button").click(function(){
   button = $(this)
   var payload = button.data('payload');
   var room_url = button.attr('data-url');
   var status_url = $("#gauge_container").attr('data-status');
   $.ajax({
     url: room_url,
     dataType: 'json',
     data: { payload: payload },
     success: function (data) {
       update_needle();
     }
     });
  });

  function update_needle() {
    var status_url = $("#gauge_container").attr('data-status');
    $.ajax({
      url: status_url,
      dataType: 'json',
      success: function (data) {
        gauge.set(data.percent);
        $("#attendee_count").text(data.attendees);
        $("#vote_count").text(data.votes)
        if (data.able_to_vote == false){
          $("#vote_thumbs_up").addClass('disabled');
          $("#vote_thumbs_down").addClass('disabled');
        }else{
          $("#vote_thumbs_up").removeClass('disabled');
          $("#vote_thumbs_down").removeClass('disabled');
        }
      }
    })
    return true;              // The function returns the product of p1 and p2
  }
});
