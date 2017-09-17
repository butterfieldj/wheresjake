#import mongo_data
from sanic import Sanic
from sanic.response import json
from sanic import response
import os

app = Sanic(__name__)

@app.route('/history', methods=['GET'])
async def get_locations(request):
    history = mongo_data.get_location_history()
    for h in history:
        del h['_id']
    return json({
        'locations': history
    })

@app.route('/location', methods=['GET'])
async def get_location(request):
    location = mongo_data.get_last_location()
    return json({
        'latitude': location['latitude'],
        'longitude': location['longitude'],
        'address': location.get('address'),
        'time': location['time']
    })

@app.route('/location', methods=['POST'])
async def set_location(request):
    mongo_data.set_location(request.json['latitude'], request.json['longitude'])
    return json({'status':'success'})

@app.route('/login', methods=['GET'])
async def get_login_page(request):
    return await response.file('./static/login.html')

@app.route('/login', methods=['POST'])
async def login(request):
    print(request.form['name'][0])
    if 'name' in request.form and request.form['name'][0] == 'Roxana':
        resp = response.redirect('/home')
        resp.cookies['tkn'] = '123'
        return resp
    else:
        return await response.file('./static/login.html')

@app.route('/home', methods=['GET'])
async def home(request):
    return await response.file('./static/index.html')

@app.middleware('request')
async def authenticate(request):
    if ((request.cookies.get('tkn') == None or 
        request.cookies.get('tkn') != '123') and
        request.path != '/login'):
        return response.redirect('/login')

app.static('/', './static')

app.run(host="0.0.0.0", port=8000, debug=True)
