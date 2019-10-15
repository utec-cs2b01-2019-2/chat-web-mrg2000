
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
    if(user_from_id != data[i]['id']){
    user_to = data[i]['id'];
    e = '<li class="contact" onclick="load_user_messages('+user_to+','+user_from_id+')"><div class="wrap"> <span class="contact-status online"></span> <img src="static/images/'+data[i]['username'] +'.jpg" /><div class="meta"><p class="name">'+data[i]['username']+'</p><p class="preview">You just got LITT up, Mike.</p></div></div></li>';
    $("<li>",{html:e}).appendTo("#users");
    }
        i = i+1;
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
    $("#messages").empty();
    $("#boton").empty();
    header_chat(user_to_id);
    boton = '<button class="submit" onclick="send_messages('+user_from_id+','+user_to_id+')">Enviar</button> <!--<i class="fa fa-paper-plane" aria-hidden="true"></i>-->'
    $("#boton").append(boton);
    var url = "/messages/"+user_from_id+"/"+user_to_id;
    $.getJSON(url,function(data){
    console.log(data);
    console.log("Trayendo los mensajes de "+user_from_id+" y "+user_to_id);
    console.log("Mensajes esta vacio ? "+jQuery.isEmptyObject(data))
    if(jQuery.isEmptyObject(data)){
    $("<div>",{html:"<p>ESTE CHAT ESTA VACIO, INICIE UNA CONVERSACION PARA VISUALIZAR EL CONTENIDO</p>"}).appendTo("#messages");
    }else{
    var i=0;
    $.getJSON("/current", function(info){
    current = info['id']
    $.each(data,function(){
    content = data[i]['content'];
    user = data[i]['user_to_id'];
    if(user != current){
    e = '<ul id="mensajes"><li class="sent"> <img src="static/images/'+data[i]['user_from'] +'.jpg" alt="" /> <p>'+content+'</p></li></ul>'
    i = i+1;
    $("<div>",{html:e}).appendTo("#messages");
    }else{
    e = '<ul id="mensajes"><li class="replies"> <img src="static/images/'+data[i]['user_from'] +'.jpg" alt="" /> <p>'+content+'</p></li></ul>'
    i = i+1;
    $("<div>",{html:e}).appendTo("#messages");
    }
    $('#messages').scrollTop( $('#messages').prop('scrollHeight') );
    });
    })};
    });
}


function info_user(){

    console.log("Informacion del usuario");

    $.getJSON("/current", function(data){
    var i=0;
    console.log(data);
    nombre = data['username'];
    e = '<div><img id="profile-img" src="static/images/'+nombre+'.jpg" class="online" alt="" /><p>'+nombre+'</p></div>'
    i = i+1;
    $("#nombre_usuario").append(e);
    });
}


function send_messages(user_from_id,user_to_id){
var content = $('#text-input').val();
if(content != ''){
    var message = JSON.stringify({
    "content": content,
    "user_from_id": user_to_id,
    "user_to_id": user_from_id
    });
    console.log(message);

 $.ajax({
    url: '/messagesjson',
    type: 'POST',
    contentType: 'aplication/json',
    data: message,
    dataType: 'json'
 });
 document.getElementById("text-input").value = "";
 load_user_messages(user_to_id,user_from_id);
}}


function header_chat(user_id){
$.getJSON("/users/"+user_id, function(data){
    nombre = data['username']
    console.log("Header chat");
    $("#header_chat").empty();
    e = '<img src="static/images/'+nombre+'.jpg" alt="" /><p>'+nombre+'</p>'
    $("#header_chat").append(e);
    });
}