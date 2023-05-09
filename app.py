from flask import Flask, render_template,flash,redirect,url_for,sessions,redirect,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt

#! Kullanıcı Kayıt Formu
class RegisterForm(Form):
    name = StringField("İsim Soyisim", validators=[validators.Length(min=4,max=25)])
    username = StringField("Kullanıcı Adı", validators=[validators.Length(min=5,max=35)])
    email = StringField("Email Adresi", validators=[validators.Email(message="Lütfen Geçerli bir email adresi giriniz")])
    password = PasswordField("Paralo", validators=[validators.DataRequired(message="Lütfen bir paralo giriniz"),
                                                   validators.EqualTo(fieldname="confirm",message="Parolanız uyuşmuyor.")])
    confirm = PasswordField("Parola Doğrula")
app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "testblog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html',answer = "evet")

@app.route('/about')
def about():
    return render_template('about.html')

#! REGISTER TAB-------------------------------------------------
@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    
    if request.method == 'POST' and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)
        
        cursor = mysql.connection.cursor()
        
        sorgu = "Insert into users (name, email, username, password) VALUES (%s,%s,%s,%s)"
        
        cursor.execute(sorgu,(name,email,username,password))
        mysql.connection.commit()
        
        cursor.close()
        
        return redirect(url_for("index"))
    else:
        return render_template("register.html",form=form)

if __name__ == '__main__':
    app.run(debug=True)

