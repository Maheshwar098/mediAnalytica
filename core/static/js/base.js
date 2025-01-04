var cookieArr = document.cookie.split("; ")
var typeCookie = cookieArr.at(-1)
var type = typeCookie.slice(5,typeCookie.length)
var logoutForm = document.getElementById("logoutForm")
logoutForm.action = "/"+type+"/logout"
function checkAuthentication(targetUrl, event){
    console.log("ahh shit", event)
    event.preventDefault()
    
    var cookieArr = document.cookie.split("; ")
    is_logged_in = false
    for(var i = 0 ; i < cookieArr.length ; i++){
        key = cookieArr[i].slice(0,4)
        if(key === "type"){
            is_logged_in = true;
            break
        }
    }
    if(!is_logged_in){
        alert("Please login to continue")
    }
    else{
        window.location.href = targetUrl;
    }
}