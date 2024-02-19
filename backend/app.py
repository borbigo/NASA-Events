from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime
import requests

app = Flask(__name__)
cors = CORS(app)

EONET_API_URL = 'https://eonet.gsfc.nasa.gov/api/v3/events'

@app.route('/api/events', methods=['GET'])
@cross_origin()
def get_events():
    try:
        response = requests.get(EONET_API_URL)
        if response.status_code == 200:
          events_data = response.json()['events']
          events = [{
              'id': event['id'],
              'title': event['title'],
              'description': event['description'],  # Add description field
              'categories': [category['title'] for category in event['categories']],
              'date': format_date(event['geometry'][0]['date']),
              'location': event['geometry'][0]['coordinates'][::-1],  # Reverse coordinates for lat, lon format
              'link': event['sources'][0]['url'] if event['sources'] else ''
          } for event in events_data]
          return jsonify(events)
        else:
            return jsonify({'error': 'Failed to fetch events from EONET API'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def format_date(date_string):
  # Parse the date string into datetime object
  date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
  # format into MM/DD/YYYY 
  formatted_date = date_object.strftime('%m/%d/%Y')
  return formatted_date
  

if __name__ == '__main__':
    app.run(debug=True)
