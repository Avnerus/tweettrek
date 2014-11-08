try {
   var autobahn = require('autobahn');
} catch (e) {
   // when running in browser, AutobahnJS will
   // be included without a module system
}

var container;

var connection = new autobahn.Connection({
   url: 'ws://127.0.0.1:8080/ws',
   realm: 'realm1'}
);

connection.onopen = function (session) {

    console.log("Opened connection");

    function on_heartbeat(args, kwargs, details) {
       console.log("Got heartbeat (publication ID " + details.publication + ")");
    }

    session.subscribe('com.myapp.heartbeat', on_heartbeat);

   function on_tweet(args, kwargs) {
      console.log("Got event:", args, kwargs);
      var p = document.createElement("p");
      var t = document.createTextNode(kwargs.data.text);
      p.appendChild(t);
      container.appendChild(p);
      p.scrollIntoView();
   }

   console.log(on_tweet);
   session.subscribe('com.tweettrek.tweet', on_tweet);
};

window.onload = function() {
    container = document.getElementById("tweets-container");
    connection.open();
}

