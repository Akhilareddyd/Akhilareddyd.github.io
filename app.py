from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city_name = request.form.get('city')
        r = requests.get('https://api.openweathermap.org/data/2.5/weather?q=' + city_name + '&appid=78d05499d9dd0e5750c1671b6fb606e4')

        if r.status_code == 200:
            try:
                json_object = r.json()
                temperature = int(json_object.get('main', {}).get('temp', 0) - 273.15)
                humidity = int(json_object.get('main', {}).get('humidity', 0))
                pressure = int(json_object.get('main', {}).get('pressure', 0))
                wind = int(json_object.get('wind', {}).get('speed', 0))
                condition = json_object['weather'][0]['main']
                desc = json_object['weather'][0]['description']

                return render_template('index.html', temperature=temperature, pressure=pressure, humidity=humidity,
                                       city_name=city_name, condition=condition, wind=wind, desc=desc)
            except KeyError as e:
                error_message = f"Error: {e}"
                return render_template('index.html', error_message=error_message), 500
        else:
            json_object = r.json()
            if json_object.get('message') == 'city not found':
                error_message = f"Error: City '{city_name}' not found"
                return render_template('index.html', error_message=error_message), 500
            else:
                error_message = f"Error: Unable to retrieve weather data. Status code: {r.status_code}"
                return render_template('index.html', error_message=error_message), 500
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

    app.run(debug=True)
