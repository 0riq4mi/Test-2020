from flask import Flask, render_template,flash,redirect,url_for,session,redirect,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps

#! Kullanıcı Giriş Decoratır'ı
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("You must be logged in","danger")
            return redirect(url_for("login"))
    return decorated_function

#! Kullanıcı Kayıt Formu
class RegisterForm(Form):
    name = StringField("İsim Soyisim", validators=[validators.Length(min=4,max=25)])
    username = StringField("Kullanıcı Adı", validators=[validators.Length(min=5,max=35)])
    email = StringField("Email Adresi", validators=[validators.Email(message="Lütfen Geçerli bir email adresi giriniz")])
    password = PasswordField("Paralo", validators=[validators.DataRequired(message="Lütfen bir paralo giriniz"),
                                                   validators.EqualTo(fieldname="confirm",message="Parolanız uyuşmuyor.")])
    confirm = PasswordField("Parola Doğrula")
    
class LoginForm(Form):
    username = StringField("Username")
    password = PasswordField("Password")

app = Flask(__name__)
app.secret_key = "testblog"

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

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

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
        flash("Başarılı bir şekilde kayıt olundu.","success")
        
        return redirect(url_for("login"))
    else:
        return render_template("register.html",form=form)

#!Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password_entered = form.password.data
        
        cursor = mysql.connection.cursor()
        
        sorgu = "Select * From users where username=%s"
        
        result = cursor.execute(sorgu,(username,))
        
        if result > 0:
            data = cursor.fetchone()
            real_password = data["password"]
            if sha256_crypt.verify(password_entered,real_password):
                flash("Başarılı bir şekilde giriş yapıldı.","success")
                
                session["logged_in"] = True
                session["username"] = username
                
                return redirect(url_for("index"))
            else:
                flash("Parolanızı yalnış girdiniz.","danger")
                return redirect(url_for("login"))

        else:
            flash("Böyle Bir kullanıcı bulunmuyor...","danger")
            return redirect(url_for("login"))
        
    
        
    return render_template('login.html',form=form)

#!Logout Page
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)

