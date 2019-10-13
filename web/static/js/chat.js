
function get_current_user(){
    console.log("CURRENT USER")
    $.getJSON("/current", function(data){
    console.log("Current user is "+data['username']+ " y su id es "+data['id'])
    user_from = data['id']
    get_all_users(user_from)
    });
}





function get_all_users(user_from_id){
    console.log("Trayendo usuarios");

    $.getJSON("/users", function(data){
    var i=0;

    $.each(data, function(){
    user_to = data[i]['id'];
    e = '<li class="contact" onclick="load_user_messages('+user_to+','+user_from_id+')"><div class="wrap"> <span class="contact-status online"></span> <img src="static/images/'+data[i]['username'] +'.jpg" /><div class="meta"><p class="name">'+data[i]['username']+'</p><p class="preview">You just got LITT up, Mike.</p></div></div></li>';
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


function load_user_messages(user_to_id,user_from_id){
    console.log("Trayendo mensajes");
    $("#messages").empty()
    $.getJSON("/messages/"+user_from_id+"/"+user_to_id,function(data){
    console.log("Trayendo los mensajes de "+user_from_id+" y "+user_to_id);
    console.log("Mensajes esta vacio ? "+jQuery.isEmptyObject(data))
    if(jQuery.isEmptyObject(data)){
    $("<div>",{html:"<p>ESTE CHAT ESTA VACIO, INICIE UNA CONVERSACION PARA VISUALIZAR EL CONTENIDO</p>"}).appendTo("#messages");
    }else{
    var i=0;
    $.each(data,function(){
    content = data[i]['content'];
    e = '<ul id="mensajes"><li class="sent"> <img src="static/images/'+data[i]['user_from'] +'.jpg" alt="" /> <p>'+content+'</p></li></ul>'
    i = i+1;
    $("<div>",{html:e}).appendTo("#messages");
    });
    }
    });
}