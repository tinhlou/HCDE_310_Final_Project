from flask import Flask, render_template
import requests
import json

app = Flask(__name__, template_folder='templates', static_url_path='/static')

growstuff_crops_url = "https://www.growstuff.org/crops.json"

with open('plant_info.json', 'r') as file:
    plant_info = json.load(file)

@app.route('/')
def index():

    seasons = [
        {'name': 'Spring', 'endpoint': 'spring'},
        {'name': 'Summer', 'endpoint': 'summer'},
        {'name': 'Fall', 'endpoint': 'fall'},
        {'name': 'Winter', 'endpoint': 'winter'}
    ]
    return render_template('index.html', seasons=seasons)

def fetch_plant(season_name, crop_names):
    try:
        response = requests.get(growstuff_crops_url)

        if response.status_code == 200:
            crops_data = response.json()

            with open('plant_info.json', 'r') as file:
                plant_info = json.load(file)

            filter_crops = []
            for crop in crops_data:
                if crop['name'] in crop_names:
                    crop_info = {
                        'name': crop['name'],
                        'description': plant_info.get(crop['name'].lower(), {}).get('description', crop['description']),
                        'thumbnail_url': crop.get('thumbnail_url', ''),
                        'life_span': plant_info.get(crop['name']. lower(), {}).get('life_span', 'N/A'),
                        'care_tips': plant_info.get(crop['name'].lower(), {}).get('care_tips', 'N/A'),
                        'planting_info': plant_info.get(crop['name'].lower(), {}).get('planting_info', 'N/A'),
                        'harvest_info': plant_info.get(crop['name'].lower(), {}).get('harvest_info', 'N/A'),
                        'start_planting_indoors': plant_info.get(crop['name'].lower(), {}).get('start_planting_indoors', ' '),
                        'transplant_date': plant_info.get(crop['name'].lower(), {}).get('transplant_date', 'N/A'),
                        'start_planting_outdoors': plant_info.get(crop['name'].lower(), {}).get('start_planting_outdoors', 'N/A'),
                    }
                    filter_crops.append(crop_info)

            return render_template('season.html', season_name=season_name, crops=filter_crops)

        else:
            return render_template('error.html', status_code=response.status_code)

    except requests.RequestException as e:
        return render_template('error.html', error_message=str(e))


@app.route('/spring')
def spring():
    return fetch_plant('Spring', {'tomato', 'beet', 'radish', 'carrot', 'potato'})
@app.route('/summer')
def summer():
    return fetch_plant('Summer', {'squash', 'eggplant', 'strawberry'})
@app.route('/fall')
def fall():
    return fetch_plant('Fall', {'lettuce', 'broccoli', 'cauliflower', 'spinach', 'kale'})
@app.route('/winter')
def winter():
    return fetch_plant('Winter', {'brussel sprouts', 'shallot', 'cabbage', 'lettuce'})

if __name__ == '__main__':
    app.run(debug=True)