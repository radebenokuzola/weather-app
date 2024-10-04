from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace with your actual OpenWeather API key and Google API details
API_KEY = '98a5709aec183251b7653340d5ea52ba'
GOOGLE_API_KEY = 'AIzaSyC54SVLr2QpT2VHZloXNgaL5YHxH4RVHmI'
SEARCH_ENGINE_ID = '71f272056fad849fe'  # Corrected the trailing quote

# Function to fetch city image using Google Custom Search
def fetch_city_image(city_name):
    search_url = f"https://www.googleapis.com/customsearch/v1?q={city_name}&searchType=image&key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}"
    response = requests.get(search_url)
    data = response.json()

    # Check if the response contains image data
    if 'items' in data:
        image_url = data['items'][0]['link']  # Get the first image link
        return image_url
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    # Get the city name from the form input
    city = request.form['city']

    # Construct the API URL with the city name and API key
    api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'

    # Make a request to the OpenWeather API
    response = requests.get(api_url)
    data = response.json()

    # Parse the JSON data returned by the API
    if response.status_code == 200:
        weather_data = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'image_url': fetch_city_image(city)  # Fetch the image URL using your Google API
        }
        return render_template('weather_result.html', weather=weather_data)
    else:
        error_message = data.get('message', 'City not found.')
        return render_template('index.html', error=error_message)

if __name__ == '__main__':
    app.run(debug=True)



