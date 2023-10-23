import requests
import gradio as gr
api_key = 'f2f6425a67514f128a0806765cff28a2'
def geocode_location(location):
    base_url = 'https://api.opencagedata.com/geocode/v1/json'
    params = {
        'q': location,
        'key': api_key,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if 'results' in data and data['results']:
        # Extract latitude and longitude from the first result
        first_result = data['results'][0]
        lat = first_result['geometry']['lat']
        lon = first_result['geometry']['lng']
        return lat, lon
    else:
        return None

def get_nearest_hospitals(city,country, radius=5000):
    location=city+','+country
    coordinates=geocode_location(location)

    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    (
        node["amenity"="hospital"](around:{radius},{coordinates[0]},{coordinates[1]});
        way["amenity"="hospital"](around:{radius},{coordinates[0]},{coordinates[1]});
        relation["amenity"="hospital"](around:{radius},{coordinates[0]},{coordinates[1]});
    );
    out center;
    """
    response_overpass = requests.get(overpass_url, params={'data': query})
    data_location = response_overpass.json()
    result=''
    for item in data_location['elements']:
        if 'tags' in item:
            result = f"Name: {item['tags'].get('name', 'N/A')}\n"

    # Check if 'lat' and 'lon' exist before adding them to the result


    return result
interface=gr.Interface(get_nearest_hospitals,inputs=['text','text'],outputs=['text'],title='Nearest Hospitals finder for Medium/Severe Conditions',description='Enter your city and location to get nearest hopsitals if condition is Medium/Severe')
interface.launch(share=True)

