from flask import Flask, render_template, flash, url_for, redirect, sessions, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

#Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Lucek123'
app.config['MYSQL_DB'] = 'usms'
app.config['MYSQL_CURSSORCLASS'] = 'DictCursor'
#Init MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [validators.Length(min=5, max=50),
                                          validators.Required(),
                                          validators.EqualTo('confirm', message='Password do not match')])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))

        #Create cursor
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO users(name, email, username, password) VALUES (%s, %s, %s, %s)", (name, email, username, password))
        mysql.connection.commit()

        cur.close()

        flash("You are now registered and ca log in", 'success')

        return redirect(url_for('index'))
    return render_template('register.html', form=form)
if __name__ == '__main__':
    app.secret_key='secret_key123'
    app.run(debug=True)
