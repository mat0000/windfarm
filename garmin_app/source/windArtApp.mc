using Toybox.Application as App;
using Toybox.WatchUi as Ui;
using Toybox.System;
using Toybox.Communications;
using Toybox.Lang as Lang;



const URL = "https://api.data.gov.sg/v1/environment/wind-speed";

class windArtApp extends App.AppBase {

    function initialize() {
        AppBase.initialize();
    }

    // onStart() is called on application start up
    function onStart(state) {
      
    }

    // onStop() is called when your application is exiting
    function onStop(state) {
    }

    // Return the initial view of your application here
    function getInitialView() {
        return [ new windArtView("Starting ") ];
    }

   
}