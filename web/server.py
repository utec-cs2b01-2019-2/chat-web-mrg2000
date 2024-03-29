from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import datetime
import json
import time

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

#Comunicacion StateLess / NO tiene memoria
@app.route('/cuantasletras/<nombre>') #Le asigna <nombre> a la variable 'cuantasletras'
def cuantas_letras(nombre):
    return str(len(nombre)) #Se retorna un string de la longitud de nombre

#Comunicacion StateFul / SI tiene memoria
@app.route('/suma/<numero>') #Le asigna <nombre> a la variable 'cuantasletras'
def suma(numero):

    if 'suma' not in session:
        session['suma'] = 0

    suma = session['suma'] #Session es un diccionario diseñado en la libreria Flask
    suma = suma + int(numero)
    session['suma'] = suma #Se inserta en el diccionario bajo la clave suma el valor
    return str(suma)
    #Se retorna un string con la suma


#Login con metodo post
@app.route('/login' , methods =['POST']) #Como se puede utilizar mas de un metodo, se recibibe un arreglo
def login():
    #El metodo crea un diccionario en donde la clave es el nombre del input y el valor es el contenido ingresado
    username = request.form['user'] #Le asignamos a la variable username lo ingresado en el formulario insertado en el html
    password = request.form['password']

    db_session = db.getSession(engine)

    user = db_session.query(entities.User).filter(
        entities.User.username == username
    ).filter(
    entities.User.password == password
    ).first()

    if user != None:
        session['usuario'] = username
        session['logged_user'] = user.id
        return render_template('chat.html')
    else:
        return "Sorry "+username+" no esta en la base de datos"



@app.route('/users', methods = ['POST'])
def create_userDevExtream():
    c =  json.loads(request.form['values'])
    #c = json.loads(request.data)
    user = entities.User(
        username=c['username'],
        name=c['name'],
        fullname=c['fullname'],
        password=c['password']
    )
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    return 'Created User'

@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        js = json.dumps(user, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { 'status': 404, 'message': 'Not Found'}
    return Response(message, status=404, mimetype='application/json')

@app.route('/users', methods = ['GET'])
def get_users():
    session = db.getSession(engine)
    dbResponse = session.query(entities.User)
    data = dbResponse[:]
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/users/<id>', methods = ['PUT'])
def update_user(id):
    session = db.getSession(engine)
    #id = request.form['key']
    user = session.query(entities.User).filter(entities.User.id == id).first()
    #c = json.loads(request.form['values'])
    c = json.loads(request.data) #Cambio para no usar Json
    for key in c.keys():
        setattr(user, key, c[key])
    session.add(user)
    session.commit()
    return 'Updated User'

@app.route('/users', methods = ['PUT'])
def update_userDevExtream():
    session = db.getSession(engine)
    id = request.form['key']
    user = session.query(entities.User).filter(entities.User.id == id).first()
    c = json.loads(request.form['values'])
    for key in c.keys():
        setattr(user, key, c[key])
    session.add(user)
    session.commit()
    return 'Updated User'

@app.route('/users/<id>', methods = ['DELETE'])
def delete_user(id):
    #id = request.form['key']
    session = db.getSession(engine)
    user = session.query(entities.User).filter(entities.User.id == id).one()
    session.delete(user)
    session.commit()
    return "Deleted User"

@app.route('/users', methods = ['DELETE'])
def delete_userDevExtream():
    id = request.form['key']
    session = db.getSession(engine)
    user = session.query(entities.User).filter(entities.User.id == id).one()
    session.delete(user)
    session.commit()
    return "Deleted User"

@app.route('/create_test_users', methods = ['GET'])
def create_test_users():
    db_session = db.getSession(engine)
    user = entities.User(name="David", fullname="Lazo", password="1234", username="qwerty")
    db_session.add(user)
    db_session.commit()
    return "Test user created!"


@app.route('/messages', methods = ['POST'])
def create_message():
    c = json.loads(request.form['values'])
    message = entities.Message(
        content=c['content'],
        sent_on=datetime.datetime(2000,2,2),
        user_from_id=c['user_from_id'],
        user_to_id=c['user_to_id']
    )
    session = db.getSession(engine)
    session.add(message)
    session.commit()
    return 'Created Message'

@app.route('/messagesjson', methods = ['POST'])
def create_messagejson():
    c = json.loads(request.data)
    message = entities.Message(
        content=c['content'],
        sent_on=datetime.datetime(2000,2,2),
        user_from_id=c['user_from_id'],
        user_to_id=c['user_to_id']
    )
    session = db.getSession(engine)
    session.add(message)
    session.commit()
    return Response(json.dumps(message), status=201, mimetype='application/json')

@app.route('/messages/<id>', methods = ['GET'])
def get_message(id):
    db_session = db.getSession(engine)
    messages = db_session.query(entities.Message).filter(entities.Message.id == id)
    for message in messages:
        js = json.dumps(message, cls=connector.AlchemyEncoder)
        return Response(js, status=200, mimetype='application/json')

    message = {'status': 404, 'message': 'Not Found'}
    return Response(message, status=404, mimetype='application/json')

@app.route('/messages', methods = ['GET'])
def get_messages():
    sessionc = db.getSession(engine)
    dbResponse = sessionc.query(entities.Message)
    data = dbResponse[:]
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/messages/<user_from_id>/<user_to_id>', methods = ['GET'])
def get_messages_user(user_from_id, user_to_id ):
    db_session = db.getSession(engine)
    messages_send = db_session.query(entities.Message).filter(
        entities.Message.user_from_id == user_from_id).filter(
        entities.Message.user_to_id == user_to_id
    )
    messages_recieved = db_session.query(entities.Message).filter(
        entities.Message.user_from_id == user_to_id).filter(
        entities.Message.user_to_id == user_from_id
    )
    data = []
    for message in messages_send:
        data.append(message)
    for message in messages_recieved:
        data.append(message)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/messages', methods = ['PUT'])
def update_message():
    session = db.getSession(engine)
    id = request.form['key']
    message = session.query(entities.Message).filter(entities.Message.id == id).first()
    c = json.loads(request.form['values'])
    for key in c.keys():
        setattr(message, key, c[key])
    session.add(message)
    session.commit()
    return 'Updated Message'

@app.route('/messages', methods = ['DELETE'])
def delete_message():
    id = request.form['key']
    session = db.getSession(engine)
    message = session.query(entities.Message).filter(entities.Message.id == id).one()
    session.delete(message)
    session.commit()
    return "Deleted Message"

@app.route('/create_test_messages', methods = ['GET'])
def create_test_messages():
    db_session = db.getSession(engine)
    message = entities.Message(content="Hi")
    db_session.add(message)
    db_session.commit()
    return "Test message created!"

@app.route('/sendMessage', methods = ['POST'])
def send_message():
    message = json.loads(request.data)
    content = message['content']
    user_from_id = message['user_from_id']
    user_to_id = message['user_to_id']
    session = db.getSession(engine)
    add = entities.Message(
    content=content,
    sent_on=datetime.datetime(2000, 2, 2),
    user_from_id=user_from_id,
    user_to_id=user_to_id,

    )
    session.add(add)
    session.commit()
    return 'Message sent'

@app.route('/authenticate', methods = ['POST'])
def authenticate():
    #Get data form request
    #time.sleep(3)
    message = json.loads(request.data)
    username = message['username']
    password = message['password']

    # Look in database
    db_session = db.getSession(engine)

    try:
        user = db_session.query(entities.User
            ).filter(entities.User.username==username
            ).filter(entities.User.password==password
            ).one()
        session['logged_user'] = user.id
        message = {'message':'Authorized','user_id':user.id,'username':user.username}
        return Response(json.dumps(message), status=200,mimetype='application/json')
    except Exception:
        message = {'message':'Unauthorized'}
        return Response(json.dumps(message), status=401,mimetype='application/json')

@app.route('/usuarios', methods=['GET'])
def todos_los_usuarios():
    db_session = db.getSession(engine)
    users = db_session.query(entities.User)
    response = ""
    for user in users:
        response += " "+user.username + " - " +user.password

    return response


@app.route('/current', methods = ['GET'])
def current_user():
    db_session = db.getSession(engine)
    user = db_session.query(entities.User).filter(entities.User.id == session['logged_user']).first()
    return Response(json.dumps(user,cls=connector.AlchemyEncoder),mimetype='application/json')

@app.route('/logout', methods = ['GET'])
def logout():
    session.clear()
    return render_template('login.html')


#API de Grupos
#1. La de crear grupos
@app.route('/grupos', methods = ['POST'])
def create_group():
    c = json.loads(request.data)
    group = entities.Group(
        name = c['name']
    )

    session_db = db.getSession(engine)
    session_db.add(group)
    session_db.commit()
    return 'Created group'

#2. Leer grupos
@app.route('/grupos/<id>', methods = ['GET'])
def read_grupos(id):
    session_db = db.getSession(engine)
    group = session_db.query(entities.Group).filter(
        entities.Group.id == id).first()
    data = json.dumps(group, cls=connector.AlchemyEncoder)
    return Response(data,status=200, mimetype='application/json')

#3. Mostrar todos los grupos
@app.route('/grupos', methods = ['GET'])
def get_all_grupos():
    session_db= db.getSession(engine)
    dbResponse = session_db.query(entities.Group)
    data = dbResponse[:]
    return Response(json.dumps(data,cls=connector.AlchemyEncoder),mimetype='application/json')


#4. Update grupo
@app.route('/grupos/<id>', methods = ['PUT'])
def update_grupo(id):
    session = db.getSession(engine)
    group = session.query(entities.Group).filter(entities.Group.id == id).first()
    c = json.loads(request.data)
    for key in c.keys():
        setattr(group, key, c[key])
    session.add(group)
    session.commit()
    return 'Updated Group'



#5. Delete grupo
@app.route('/grupos/<id>', methods = ['DELETE'])
def delete_grupo(id):
    session = db.getSession(engine)
    group = session.query(entities.Group).filter(entities.Group.id == id).one()
    session.delete(group)
    session.commit()
    return "Deleted Group"




if __name__ == '__main__':
    app.secret_key = ".."
    app.run(debug=True,port=8000, threaded=True, use_reloader=False)
