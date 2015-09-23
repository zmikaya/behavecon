// counter spinner does not allow negatve integers
(function ($) {
  $('.spinner .btn:first-of-type').on('click', function() {
    $('.spinner input').val( parseInt($('.spinner input').val(), 10) + 1);
  });
  $('.spinner .btn:last-of-type').on('click', function() {
      if (parseInt($('.spinner input').val(), 10) > 0) {
        $('.spinner input').val( parseInt($('.spinner input').val(), 10) - 1);
      }
  });
})(jQuery);

// make session type button responsive
$(".dropdown-item").click(
  function(){
    $("#sessionType").text(this.innerHTML)
    $("#sessionType").append('<span class="caret"></span>')
  })
  
  
// enable "create session" button only after all requirements are met
function ensureRequirements(){
  var flag1 = false;
  var flag2 = false;
  var flag3 = false;
  // check "session name"
   ($("#inputName")).change(
    function(){
      if ($("#inputName").val().length > 0){
        flag1 = true;
      }
      else {
        flag1 = false;
      }
      changeButtonCSS([flag1, flag2, flag3])
    })
  // check group size
  $('.spinner').change(
    function(){
      if ($.isNumeric($('.spinner input').val()) && parseInt($('.spinner input').val(), 10) > 0){
        flag2 = true;
      }
      else {
        flag2 = false;
      }
      changeButtonCSS([flag1, flag2, flag3])
    })
  $('.spinner .btn').on('click',
    function(){
      if ($.isNumeric($('.spinner input').val()) && parseInt($('.spinner input').val(), 10) > 0){
        flag2 = true;
      }
      else {
        flag2 = false;
      }
      changeButtonCSS([flag1, flag2, flag3])
    })
  // check session type
  $(".dropdown-menu").on('click',
    function(){
      if ($("sessionType").text().trim() != "Session Type"){
        flag3 = true;
      }
      else {
        flag3 = false;
      }
      changeButtonCSS([flag1, flag2, flag3])
    })
    
}

function changeButtonCSS(flags){
  for (var i=0; i<flags.length; i++){
    if (flags[i] == false){
      if (!$("#createSession").hasClass("disabled")){
        $("#createSession").addClass("disabled")
      }
      break
    }
    if (i==2 && $("#createSession").hasClass("disabled")){
      $("#createSession").removeClass("disabled")
    }
  }
}

ensureRequirements()

// end

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// create a session
function createSession(){
    var csrftoken = getCookie('csrftoken');
    var stype = getSType($("#sessionType").text())
    $.ajax({
      type: "POST",
      url: "/create_session",
      data: {
          'csrfmiddlewaretoken': csrftoken,
          'sessionName': $("#inputName").val(),
          'players': $("#spinner").val(),
          'sessionType': stype
        },
        success: updateSessions,
        dataType: 'html'
    });
};

function getSType(name){
  var stype = 0;
  if (name == "Category 3Dams"){
    stype = 0;
  }
  else if (name == "Free 3Dams"){
    stype = 1;
  }
  else {
    stype = 2;
  }
  return stype
}

// handles the returned html/data from Django
// clears existing body, then replaces it with returned html
function updateSessions(data, textStatus, jqXHR){
    var data = $.parseHTML(data);
    // $("tr.hoverable").empty()
    for (var i=0; i<data.length; i++){
      $("#session_list").append(data[i])
    }
}
// end

// end a session
$(".btn-danger").click(function() {
    endSession($(this).attr("id"))
})

function endSession(session){
    var csrftoken = getCookie('csrftoken');
    $.ajax({
      type: "POST",
      url: "/end_session",
      data: {
          'csrfmiddlewaretoken': csrftoken,
          'sessionName': session,
        },
        success: endSessions,
        dataType: 'html'
    });
};

function endSessions(data, textStatus, jqXHR){
}

