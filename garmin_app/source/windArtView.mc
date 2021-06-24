using Toybox.WatchUi as Ui;
using Toybox.System;
using Toybox.Communications;
using Toybox.Time.Gregorian as Gregorian;
using Toybox.Graphics as Gfx;
using Toybox.Lang as Lang;
using Toybox.Math;

class windArtView extends Ui.View {
	
    hidden var _message;
	var wind = [];
	var windCurrent = 0.0;
	var width = 200;
    var height = 130;
    var Xposition = (240 - width)/2;
    var Yposition = (240 - height)/2;
    var timeTick = 1;
    var space = 1;
    var tickWind = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50];
    var tickWindScale = tickWind;
    var windMinMax = [1000,0];

    function initialize(message) {
        View.initialize();
        _message = message;
        System.println(message);
    }

    // Load your resources here
    function onLayout(dc) {
        setLayout(Rez.Layouts.MainLayout(dc));
        // View.findDrawableById("message").setText(_message);
    }

    // Called when this View is brought to the foreground. Restore
    // the state of this View and prepare it to be shown. This includes
    // loading resources into memory.
    function onShow() {
    // some_variable =  makeRequest(0);
    // WatchUi.requestUpdate();
    makeRequest();
    }

    // Update the view
    function onUpdate(dc) {
        // Call the parent onUpdate function to redraw the layout
        View.onUpdate(dc);
		
         
        dc.clear();
		dc.setColor(Gfx.COLOR_LT_GRAY, Gfx.COLOR_TRANSPARENT);
		dc.setPenWidth(1);
		dc.drawLine(1, 1, 200, 200);
		
    }

    // Called when this View is removed from the screen. Save the
    // state of this View here. This includes freeing resources from
    // memory.
    function onHide() {
    }
    

    // set up the response callback function
   function onReceive(responseCode, data) {
   	   WatchUi.requestUpdate();
   	   wind = wind.addAll(data);
   	   windCurrent = wind[wind.size()-1];
	  //wind = [11, 12, 12, 12, 11, 1,  20, 25, 26, 27, 30, 26, 24, 23, 20, 14];
   	   // calculate only if data received
   
   }
   
  
   function makeRequest() {
        var url = "https://dreamfood.sg/get_wind";
        // var url = "http://r9.sytes.net/wind/get_wind/";
       
       // var params = null;
       
       var params = {
       	 "date_time" => "2021-06-22T15:00:00"
       	 // "date_time" => null
       };
       
       var options = {
         :method => Communications.HTTP_REQUEST_METHOD_GET,
         :responseType => Communications.HTTP_RESPONSE_CONTENT_TYPE_JSON
       };
       var responseCallback = method(:onReceive);

       Communications.makeWebRequest(url, options, params,  method(:onReceive));
  }
  
	function findWindMinMax() {
		// find min and max wind
	    for (var i = 0; i < wind.size(); i++) {
	    	if(wind[i] < windMinMax[0]) {
	    		windMinMax[0] = wind[i];
	    	}
	    	if(wind[i] > windMinMax[1]) {
	        	windMinMax[1] = wind[i];
	    	}
		}
		return(windMinMax);
	}
  
}
