from flask import Flask, render_template,flash,redirect,url_for,sessions,redirect,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt



app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "testblog"
app.config["MYSQL_CURSORCLASS"] = "Dictcursor"

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html',answer = "evet")

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)