var $messages = $('.messages-content'),
    d, h, m,
    i = 0;

$(window).load(function() {
  $messages.mCustomScrollbar();
   $.ajax({
    url:"http://127.0.0.1/reset", 
    data: "",
    type:"GET",
    success: function(result)
    { 
    }
  });
  setTimeout(function() {
    welcomeMessage();
  }, 100);
});

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
    scrollInertia: 10,
    timeout: 0
  });
}

function setDate(){
  d = new Date()
  if (m != d.getMinutes()) {
    m = d.getMinutes();
    $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
  }
}

function insertMessage() {
  msg = $('#output').val();
  if ($.trim(msg) == '') {
    return false;
  }
  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();
  // ajax the JSON to the server
  $('<div class="message loading new"><figure class="avatar"><img src="../public/images/icon.jpg" /></figure><span></span></div>').appendTo($('.mCSB_container'));
  updateScrollbar();
  txt={"query":document.getElementById('output').value}
  $.ajax({
    url:"http://127.0.0.1/receiver", 
    data: txt,
    type:"GET",
    success: function(result)
    { 
      $('.message.loading').remove();
      $('<div class="message new"><figure class="avatar"><img src="../public/images/icon.jpg" /></figure>' + result + '</div>').appendTo($('.mCSB_container')).addClass('new');
      setDate();
      updateScrollbar();
      var brsplit=result.split("<br>");
      if (result.split(":")[0]=="INFO")
      {
        movies_names = result.split(":")[1].split("=>")[1].split("<br>")[0];
        console.log(movies_names);
      }
      else
      {
        if (brsplit[0]=="Here are some commands you could try")
        {
          movies_names="Here are some commands you could try";
        }
        else if (brsplit[0].includes(":"))
        {
          console.log(brsplit);
          var movies_names="Here are "+(brsplit.length-3)+" movies for you.  ";
          for (i = 1; i<=brsplit.length-2; i++) { 
            movies_names += brsplit[i].split(" released")[0]+". . . ";
          }
        }
        else
        {
          movies_names=brsplit[0];
        }
      }
      responsiveVoice.speak(movies_names, "Hindi Female");
    }
  });
  $('#output').val("");
  updateScrollbar();
  /*setTimeout(function() {
    fakeMessage();
  }, 1000 + (Math.random() * 20) * 100);*/
}

$('.message-submit').click(function() {
  insertMessage();
});

$(window).on('keydown', function(e) {
  if (e.which == 13) {
    insertMessage();
    return false;
  }
})

var welcome = [
  'Hi there, I\'m Binger I can :<br><i>1. Recommend you movies based on your choice of Actor, Director or Genre. <br>2. Get summary of a movie for you. <br>3. Share some fun Trivias about a movie. <br>4. Find the trailer of a movie on Youtube. <br>5. Search whether a movie is on Netflix or not.</i><br>Just say \'Help Me\' whenever you need some help with the commands.',
]

function welcomeMessage() {
  if ($('.message-input').val() != '') {
    return false;
  }
  $('<div class="message loading new"><figure class="avatar"><img src="../public/images/icon.jpg" /></figure><span></span></div>').appendTo($('.mCSB_container'));
  updateScrollbar();

  setTimeout(function() {
    $('.message.loading').remove();
    $('<div class="message new"><figure class="avatar"><img src="../public/images/icon.jpg" /></figure>' + welcome[i] + '</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate();
    updateScrollbar();
  }, 1000 + (Math.random() * 20) * 100);

}

function speak(text, callback) {
    var u = new SpeechSynthesisUtterance();
    u.text = text;
    u.lang = 'en-US';
 
    u.onend = function () {
        if (callback) {
            callback();
        }
    };
 
    u.onerror = function (e) {
        if (callback) {
            callback(e);
        }
    };
 
    speechSynthesis.speak(u);
}