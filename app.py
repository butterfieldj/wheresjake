import mongo_data
from sanic import Sanic
from sanic.response import json
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

@app.middleware('request')
async def authenticate(request):
    if request.cookies.get('tkn') == None or request.cookies.get('tkn') != os.environ.get('TOKEN'):
        return json({'error': 'unauthorized'}, status=401)

app.static('/', './static')

app.run(host="0.0.0.0", port=8000, debug=True)
