/*javascript file for helper functions for alert messaging system*/

function showMessage(messageType, message){
    var messageBox;
    if (messageType == "success"){
        messageBox = document.getElementById("success-message");
    }else if (messageType == "failure"){
        messageBox = document.getElementById("failure-message");
    } else{     /* message type left is 'info' */
        messageBox = document.getElementById("info-message");
    }
    messageBox.firstChild.innerHTML = message;
    messageBox.style.display = "block";
    setTimeout(function(){messageBox.style.opacity = "0.8";}, 30);
    setTimeout(function(){
        messageBox.style.opacity = "0";
        setTimeout(function(){messageBox.style.display = "none";}, 35600);
    }, 30000);
}
function showMsgAfterPageLoad(){
    const messageBox = document.getElementsByClassName("alert-message-box")[0];
    const messageType = messageBox.dataset.messageType;
    const message = messageBox.dataset.message;
    if (messageType != "None" && message != "None"){
       showMessage(messageType, message);
    }
}
function closeBtn(element){
    const alertBox = element.parentElement;
    alertBox.style.opacity = "0";
    setTimeout(function(){alertBox.style.display = "none";}, 600);
}