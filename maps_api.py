import requests

def get_formatted_location(latitude, longitude):
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json',
                            params={'latlng': str(latitude) + ',' + str(longitude),
                                    'key': 'AIzaSyBp6fcL4vCAd5QcR5jI1PMby6qT1W2QZBc'
                                   }).json()
    if response.get('results') and len(response['results']) > 0:
        return response['results'][0]['formatted_address']
    return None
