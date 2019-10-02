function sendMessage(){
    alert("Heeee");
}


function get_all_users(){
    console.log("Trayendo usuarios");

    $.getJSON("/users", function(data){
    var i=0;

    $.each(data, function(){
    user_to = data[i]['id'];
    e = '<li class="contact"><div class="wrap"> <span class="contact-status online"></span> <img src="static/images/'+data[i]['username'] +'.jpg" /><div class="meta"><p class="name">'+data[i]['username']+'</p><p class="preview">You just got LITT up, Mike.</p></div></div></li>';
    i = i+1;
    $("<li>",{html:e}).appendTo("#users");
    });
    });
}

//{"content": "hola", "id": 1, "sent_on": null, "user_from": null, "user_from_id": 4, "user_to": null, "user_to_id": 3}
function get_all_messages(){
    console.log("Trayendo mensajes");

    $.getJSON("/messages",function(data){
    var i=0;
    content = data[i]['content'];
    $.each(data,function(){

    e = '<li class="sent"> <img src="http://emilcarlsson.se/assets/mikeross.png" alt="" /> <p>'+data[i]['content']+'</p></li>'
    i = i+1;
    $("<li>",{html:e}).appendTo("#mensajes");
    });
    });

}