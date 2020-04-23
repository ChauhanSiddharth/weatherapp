import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'


db = SQLAlchemy(app)

class City(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)

@app.route('/', methods=['GET','POST'])
def index():
	if request.method == 'POST':
		new_city = request.form.get('city')
		if new_city:
			new_city_obj = City(name=new_city)
			db.session.add(new_city_obj)
			db.session.commit()
	cities = City.query.all()

	url = 'https://api.openweathermap.org/data/2.5/find?q={}&units=imperial&appid=cba3691acaefbc861932c349b69152ec'

	weather_data = []

	for city in cities:
		r= requests.get(url.format(city.name)).json()

		weather = {
			'city' : city,
			'temperature' : r['list'][0]['main']['temp'],
			'description' : r['list'][0]['weather'][0]['description'],
			'icon' : r['list'][0]['weather'][0]['icon'],
		}

		weather_data.append(weather)

	#print(weather_data)

	return render_template('weather.html', weather_data=weather_data)

@app.route('/delete', methods=['GET'])
def delete_data():
        num_rows_deleted = db.session.query(City).delete()
        db.session.commit()
        cities = City.query.all()
        if cities:
                app.make_response("Records found")
        else:
                return redirect('/')


if __name__ == "__main__":
	app.run(debug=True)
