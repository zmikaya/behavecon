/* determine user selected responses for comparison to the correct
    responses */
var responses = {};
$("input").on( "click", 
    function() {
        $("input:checked").each(
            function(){
                var index = $(this).attr("name")[1]
                responses[index] = this.value;
            }
        )
        checkCorrect();
    }
);

var correct = ["false", "15%", "30%", "14%"];
function checkCorrect() {
    if (Object.keys(responses).length != correct.length) {
        $("#incorrect").text("You must answer all of the questions.")
    }
    else {
        for (var i=0; i<Object.keys(responses).length; i++) {
            if (responses[i] != correct[i]) {
                var num = i+1;
                $("#incorrect").text("Your answer to question " + num + " is incorrect.")
                $("#continue").removeAttr("onclick")
                // $("#continue").removeAttr("href")
                // $("#continue").attr("data-toggle", "modal")
                // $("#continue").attr("data-target", "#myModal")
                console.log('test')
                return
            }
        }
        $("#continue").attr("onclick", "ajaxGetPage('p9')")
        // $("#continue").attr("href", "/Category3Dams/p9")
        // $("#continue").removeAttr("data-toggle")
        // $("#continue").removeAttr("data-target")
        console.log("correct")
    }
}