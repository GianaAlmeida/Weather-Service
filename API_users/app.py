from flask import Flask, request, render_template
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
db = yaml.load(open('db.yaml'))

#db settings
app.config['MYSQL_HOST'] 	 = db['mysql_host']
app.config['MYSQL_USER'] 	 = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB']		 = db['mysql_db']

mysql = MySQL(app)

## Using SQL - Read
@app.route('/users/', methods=['GET'])
def home():
	cursor = mysql.connection.cursor()
	result = cursor.execute("SELECT * FROM users")
	if result > 0:
		users = cursor.fetchall()
		return render_template('index.html', users=users )

## Create
@app.route('/users/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        authorization = request.form['authorization']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users VALUES (null, %s, %s, %s);", (name, password, authorization))
        mysql.connection.commit()
        mysql.connection.close()
        return 'Sucess! :)'

## Update
@app.route('/users/update', methods=['PUT'])
def update():
    if request.method == "PUT":
        id_num = request.form['id']
        name = request.form['name']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET name = %s, password = %s WHERE id = %s;", (name, password, id_num))
        mysql.connection.commit()
        mysql.connection.close()        
        return 'Sucess! :)'

## Delete
@app.route('/users/delete', methods=['POST'])
def delete():
    if request.method == "POST":
        id_num = request.form['id']        
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s;", id_num)
        mysql.connection.commit()
        mysql.connection.close()
        return 'Sucess! :)'


if(__name__ == '__main__'):
	app.run(port = '5000', debug = True)