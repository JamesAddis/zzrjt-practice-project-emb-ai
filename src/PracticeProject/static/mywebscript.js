let RunSentimentAnalysis = ()=>{
    textToAnalyze = document.getElementById("textToAnalyze").value;
    function errorMessageResponse(message) {
        document.getElementById("system_response").innerText = message
        document.getElementById("system_response").classList.add("text-danger")
    }
    document.querySelector("button").disabled =true
    document.querySelector('input[name="textToAnalyze"]').disabled =true
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        console.log(this.readyState)
        console.log(this.status)
        if (this.readyState == 4){
            try {
                switch (this.status) {
                    case 200:
                        try {
                            document.getElementById("system_response").classList.remove("text-danger")
                            document.getElementById("system_response").innerText = xhttp.responseText
                        } catch {
                            errorMessageResponse("An error occurred after getting a success response from server!")
                        }
                        break;
                    case 400:
                    case 422:
                        try {
                            errorMessageResponse(JSON.parse(xhttp.responseText).message)
                        } catch {
                            errorMessageResponse("An error occurred after getting a validation failure response from server!")
                        }
                        break
                    default:
                        try {
                            errorMessageResponse(JSON.parse(xhttp.responseText).message)
                        } catch {
                            errorMessageResponse("An error occurred whilst getting response from server!")
                        }
                        break
                }
            } finally {
                document.querySelector("button").disabled =false
                document.querySelector('input[name="textToAnalyze"]').disabled =false
            }
        }
    };
    xhttp.open("GET", "api/sentimentAnalyzer?textToAnalyze"+"="+textToAnalyze, true);
    xhttp.send();
    return false
}
document.addEventListener("DOMContentLoaded", () => {
    console.log("Setting up overrides due to index html being rubbish");
    document.getElementsByTagName("form")[0].onsubmit =(event)=>{ event.preventDefault(); console.log("submit"); RunSentimentAnalysis(); return false;}
    document.getElementsByTagName("button")[0].onclick =(event)=>{ event.preventDefault(); console.log("click"); RunSentimentAnalysis(); return false;}
});