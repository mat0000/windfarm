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
    var timeDelay = 10;
    var space = 1;
    var tickWind = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50];
    var tickWindScale = tickWind;
    var windMinMax = [1000,0];


    function initialize(message) {
        View.initialize();
    }

    // Load your resources here
    function onLayout(dc) {
        setLayout(Rez.Layouts.MainLayout(dc));
    }

    function onShow() {
  		makeRequest();
    }

    function onUpdate(dc) {
    	View.onUpdate(dc);
		System.println( wind );
         
        dc.clear();
		dc.setColor(Gfx.COLOR_LT_GRAY, Gfx.COLOR_TRANSPARENT);
		dc.setPenWidth(1);
		
		// draw only if data are received
		if(wind.size() > 0) {
			for (var i = 0; i < wind.size(); i++) {
	    		dc.drawLine(Xposition + i * space, Yposition+height, Xposition + i * space,Yposition+height-wind[i]);
			}
	      	
	      	// draw Yticks
	      	for (var i = 0; i < tickWind.size(); i++) {
	      		dc.setColor(Gfx.COLOR_DK_GRAY, Gfx.COLOR_TRANSPARENT);
	        	dc.drawLine(Xposition, Yposition + height - tickWindScale[i], Xposition + width, Yposition + height - tickWindScale[i]);
	        	dc.setColor(Gfx.COLOR_DK_RED, Gfx.COLOR_TRANSPARENT);
	        	dc.drawText(Xposition+13, Yposition + height - tickWindScale[i]-15,Gfx.FONT_TINY, tickWind[i], Gfx.TEXT_JUSTIFY_CENTER);	
			}
			
			// daw X ticks
			var clockTime = System.getClockTime();
			var hour = clockTime.hour;
			var min = clockTime.min;
			
			
			for (var i = 0; i < 3; i++) {
			
				var tickLastHour = i;
				var tickLastHourPosition = wind.size() - min + timeDelay - (60 * i); // full hour
				if(min < timeDelay) {
					tickLastHour = hour - 1;
				} else {
					tickLastHour = hour;
				}
				dc.setColor(Gfx.COLOR_DK_GRAY, Gfx.COLOR_TRANSPARENT);
				dc.drawLine(Xposition + tickLastHourPosition * space, Yposition + 125,  Xposition + tickLastHourPosition * space, 195);
				dc.drawText(Xposition + tickLastHourPosition * space, Yposition + 130,Gfx.FONT_TINY, tickLastHour - i, Gfx.TEXT_JUSTIFY_CENTER);
			}
			
			var windTruncated = (windCurrent*10).toNumber().toFloat()/10; 
   	   		var windString = "Now: "  + windTruncated.format("%.1f") + " kmh";
			dc.setColor(Gfx.COLOR_DK_RED, Gfx.COLOR_TRANSPARENT);		
			dc.drawText(120, 20,Gfx.FONT_SMALL, windString , Gfx.TEXT_JUSTIFY_CENTER);
		} else {
			dc.setColor(Gfx.COLOR_DK_RED, Gfx.COLOR_TRANSPARENT);		
			dc.drawText(120, 100,Gfx.FONT_MEDIUM, "Loading data..." , Gfx.TEXT_JUSTIFY_CENTER);
		}
    }


    function onHide() {
    }
    
   // set up the response callback function
      function onReceive(responseCode, data) {
   	   WatchUi.requestUpdate();
   	   wind = wind.addAll(data);
   	   windCurrent = wind[wind.size()-1];

   	   // calculate only if data received
   	   if(wind.size() > 0) {
	   	   // turncate wind so width = number of reads
	        if(wind.size()-width > 0) {
	        	wind = wind.slice(wind.size()-width, wind.size());
	        }
	        
	        System.println(wind.size());
	        // find max wind
	        windMinMax = findWindMinMax();
	        System.println(windMinMax);
	
			// Find lower bound
			var myCounter = 0;
			var scaleZero = 0;
			while (tickWind[myCounter] < windMinMax[0]) {
			    scaleZero = tickWind[myCounter];
			    myCounter++;
			}
			
			// Find higher bound
			myCounter = 0;
			var scaleMax = 0;
			while (windMinMax[1] > tickWind[myCounter]) {
			    scaleMax = tickWind[myCounter+1];
			    myCounter++;
			}
			
			
			// set Yticks range
			tickWind = tickWind.slice(tickWind.indexOf(scaleZero),tickWind.indexOf(scaleMax)+1); 
			
			for (var i = 0; i < wind.size(); i++) {
	       		wind[i] = (( wind[i].toFloat() - (scaleZero)) / ((scaleMax) - (scaleZero))) * height;
	       		wind[i] = Math.round(wind[i]);
			}
			
			// scale ticks
			for (var i = 1; i < tickWind.size(); i++) {
				tickWindScale[i] = (( tickWind[i].toFloat() - (scaleZero)) / ((scaleMax) - (scaleZero))) * height;
	       		tickWindScale[i] = Math.round(tickWindScale[i]);
			}
		}
		WatchUi.requestUpdate();
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
        
   
   
   function makeRequest() {
       var url = "https://dreamfood.sg/get_wind";
       var options = {
         :method => Communications.HTTP_REQUEST_METHOD_GET,
         :responseType => Communications.HTTP_RESPONSE_CONTENT_TYPE_JSON
       };
       var responseCallback = method(:onReceive);
       Communications.makeWebRequest(url, {}, options, method(:onReceive));
  }
}