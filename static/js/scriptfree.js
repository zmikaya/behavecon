var url = "/Free3Dams/"

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


// $('.next').click(function(){
//     var csrftoken = getCookie('csrftoken');
//     var id = $("#enterid").val();
//     var page = $(this).attr('id')+'/';
//     $.ajax({
//       type: "POST",
//       url: url + page,
//       data: {
//           'id': id,
//           'csrfmiddlewaretoken': csrftoken
//         },
//         success: nextPage,
//         dataType: 'html'
//     });
// });

function dictToList(dict) {
    var keys = Object.keys(dict).sort()
    var data = [];
    for (var i=0; i<keys.length; i++) {
        data.push(dict[keys[i]]);
    }
    return data
}

function ajaxGetPage(page, data){
    var csrftoken = getCookie('csrftoken');
    console.log(url+page)
    var id = $("#enterid").val();
    // var page = $(this).attr('id')+'/';
    if (data) {
        var out = JSON.stringify(dictToList(data));
        console.log(out)
        $.ajax({
          type: "POST",
          url: url + page,
          data: {
              'data': out,
              'csrfmiddlewaretoken': csrftoken
            },
            success: nextPage,
            dataType: 'html'
        });
    }
    else {
        $.ajax({
          type: "POST",
          url: url + page,
          data: {
              'id': id,
              'csrfmiddlewaretoken': csrftoken
            },
            success: nextPage,
            dataType: 'html'
        });
    }
};

function ajaxSendData(page, data){
    var csrftoken = getCookie('csrftoken');
    console.log(url+page)
    var id = $("#enterid").val();
    // var page = $(this).attr('id')+'/';
    if (data) {
        var out = JSON.stringify(dictToList(data));
        console.log(out)
        $.ajax({
          type: "POST",
          url: url + page,
          data: {
              'data': out,
              'csrfmiddlewaretoken': csrftoken
            },
            success: emptyReturn,
            dataType: 'html'
        });
    }
}


function emptyReturn(data, textStatus, jqXHR){
    // var data = $.parseHTML(data);
    // console.log(data)
    // $("html").empty();
    // for(var i=0; i<data.length; i++){
    //     $("html").append(data[i])
    // }
    // if (tlkioOnload) {
    //     tlkioOnload();
    // }
}

// if (tlkioOnload) {
//     tlkioOnload();
// }


// handles the returned html/data from Django
// clears existing body, then replaces it with returned html
var test = null;
function nextPage(data, textStatus, jqXHR){
    test = data;
    var data = $.parseHTML(data);
    console.log(data)
    $("html").empty();
    for(var i=0; i<data.length; i++){
        $("html").append(data[i])
    }
    if (tlkioOnload) {
        tlkioOnload();
    }
}

if (tlkioOnload) {
    tlkioOnload();
}

