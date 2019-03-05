from flask import Flask
from flask.ext.pymngo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] =  'weather'
app.config['MONGO_URI'] =  'localhost:8080'

mongo = PyMongo(app)

@app.route('/create', methods=['POST'])
def create(var weather_datas):
	try:
		weather = mongo.db.weathers
		weather.insert({weather_datas})
		return 'Created';
	except: 
		return 'Something is wrong, try again'

@app.route('/read', methods=['GET'])
def read(var key, var value):
	weather = mongo.db.weathers
	try:
		answer = weather.find({key : value})
		return answer[key];
	except ValueError:
		return 'Value error: send key and value'

@app.route('/update', methods=['PUT'])
def update(var key, var value, var new_value):
	weather = mongo.db.weathers
	try:
		answer = weather.find({key : value})
		answer[key] = new_value
		weather.save(answer)
		return 'Updated';
	except ValueError:
		return 'Value error: send key, value and new value'

@app.route('/delete', methods=['POST'])
def delete(var key, var value):
	weather = mongo.db.weathers
	try:
		answer = weather.find({key : value})
		weather.remove(answer)
		return 'Removed', 200;
	except ValueError:
		return 'Value error: send key and value'

if __name__ == '__main__':
	app.run(debug:True)