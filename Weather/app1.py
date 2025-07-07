import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

WEATHER_API_KEY = '0e243f9310104062ae050605250707'  # Your weatherapi.com key

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Weather App</title>
</head>
<body>
    <h2>Weather App</h2>
    <form method="get" action="/weather">
        <input type="text" name="city" placeholder="Enter city name" required>
        <button type="submit">Get Weather</button>
    </form>
    {% if weather %}
        <h3>Weather in {{weather.city}}:</h3>
        <ul>
            <li>Temperature: {{weather.temperature}}°C</li>
            <li>Description: {{weather.description}}</li>
        </ul>
    {% elif error %}
        <p style="color: red;">{{error}}</p>
    {% endif %}
</body>
</html>
'''

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    weather = None
    error = None
    if city:
        url = f'http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                error = data["error"].get("message", "City not found or API error.")
            else:
                weather = {
                    'city': data['location']['name'],
                    'temperature': data['current']['temp_c'],
                    'description': data['current']['condition']['text'],
                }
        else:
            error = "City not found or API error."
    return render_template_string(HTML_TEMPLATE, weather=weather, error=error)

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_TEMPLATE, weather=None, error=None)

if __name__ == '__main__':
    app.run(debug=True)
