from flask import Flask, request, jsonify
from flask_caching import Cache
import json

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
app = Flask(__name__)
app.config["DEBUG"] = True
cache.init_app(app)

# Load the data into key-value pairs
# Key: star rating
# Value: list of hotel
# Then save as cache with TTL 1 minute
@cache.cached(timeout=60)
def load_data():
    file = open('data.json')
    data = json.load(file)
    star_dict = {1: [], 2: [], 3:[], 4:[], 5:[]}
    for destination in data:
        for key in destination.keys():
            for hotel in destination[key]:
                star_dict[hotel['stars']].append({'name': hotel['name'], 'stars': hotel['stars'], 'destination': key})
    return star_dict

@app.route('/hotels')
def filter():
    star_query = request.args.get('stars')
    hotels = load_data()
    response = []
    if (star_query is None) or (int(star_query) not in hotels):
        for values in hotels.values():
            response += values
    else:
        response = hotels[int(star_query)]
    return jsonify(response)

@app.route('/', methods=['GET'])
def home():
    return 'Holiday Check Assignment'

app.run()
