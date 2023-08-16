from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect

from forms import RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = b'b3374600ed4477da471589f858c5d3183ca2bd753391d4573b93bcb58321d295'
csrf = CSRFProtect(app)


@app.route('/')
def index():
    return 'Hi!'


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        password = form.password.data
        print(email, password)
        ...
    return render_template('register.html', form=form)
