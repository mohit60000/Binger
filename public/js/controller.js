$( document ).ready(function() {
  console.log('Starting SpeechRecognition library.');
  var speech = new Speech();

    speech.recognition.onstart = function() {
    $('#capture').text("Stop");
    $('#capture').val("false");
    $('#status').text("Listening...");
      console.log('Listening started...');
    }

  speech.recognition.onend = function() {
    $('#capture').text("Start");
    $('#capture').val("true");
    $('#status').text("Idle");
      console.log('Listening stopped.');
    insertMessage();
    }

  $('#capture').click(function(){
    if ($('#capture').val() == "true") {
      responsiveVoice.cancel();
      speech.startCapture();
      console.log('True');
    }
    else {
      speech.stopCapture();
      console.log('False');
    }
  });
});