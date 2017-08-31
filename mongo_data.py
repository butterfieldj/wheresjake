from pymongo import MongoClient
import pymongo
import maps_api
from datetime import datetime

client = MongoClient('localhost', 27017)
db = client.local

def get_location_history():
    return [d for d in db.location.find().sort([('_id', pymongo.DESCENDING)])] 

def get_last_location():
    return db.location.find_one()

def set_location(latitude, longitude):
    address = maps_api.get_formatted_location(latitude, longitude)
    db.location.insert_one({
        'time':datetime.now().strftime('%I:%M %P on %B, %d %Y'),
        'latitude':latitude,
        'longitude':longitude,
        'address':address
    })
