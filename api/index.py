from flask import Flask, jsonify, request, render_template, redirect
from redis import Redis
import json

app = Flask(__name__, template_folder='')

def connect_db():
    conexion = Redis(host='db-redis', port=6379, decode_responses=True)
    if(conexion.ping()):
        print("conectado a redis")
    else:
        print("error de conexion con redis")
    # conexion.flushdb()

    return conexion

def init_db():
    con = connect_db()
    if con.get('init'):
        return
    f = open('places.json')
    places = json.load(f)
    for i in range(len(places)):
        place = places[i]
        con.geoadd(place["team"], [place["longitude"], place["latitude"], place["name"]])
    con.set('init', 1)

def get_list(db, nombre_lista):
    lista = db.lrange(nombre_lista, 0, -1)
    return lista

@app.route('/', methods=['GET'])
def index():
    """Retorna la pagina index."""
    return render_template('home.html')

@app.route('/add_place', methods=['GET'])
def add_place():
    if(request.method == 'GET'):
        con = connect_db()
        team = request.args.get("team")
        name = request.args.get("name")
        latitude = request.args.get("latitude")
        longitude = request.args.get("longitude")
        con.geoadd(team, [longitude, latitude, name])
    return redirect('/')

@app.route('/places', methods=['GET'])
def places():
    places = None
    if(request.method == 'GET'):
        con = connect_db()
        team = request.args.get("team")
        latitude = request.args.get("latitude")
        longitude = request.args.get("longitude")
        places = con.georadius(team, longitude, latitude, radius=5, unit="km")
    return jsonify(places)

@app.route('/distance', methods=['GET'])
def distance():
    distance = None
    if(request.method == 'GET'):
        con = connect_db()
        latitude = request.args.get("latitude")
        longitude = request.args.get("longitude")
        team = request.args.get("team")
        name = request.args.get("name")
        toPlace = con.geopos(team, name)[0]
        if toPlace == None: return "No existe el lugar ingresado", 400
        con.geoadd("dist", [toPlace[0], toPlace[1], "1"])
        con.geoadd("dist",  [longitude, latitude, "2"])
        distance = con.geodist("dist", "1", "2", unit="km")
        con.delete('dist')
    return jsonify(distance)




if __name__ == '__main__':
    init_db()

    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='web-api-flask', port='5000', debug=True)

