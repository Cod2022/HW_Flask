# Создать форму для регистрации пользователей на сайте. 
# Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль" и кнопку "Зарегистрироваться". 
# При отправке формы данные должны сохраняться в базе данных, а пароль должен быть зашифрован.

from flask import Flask, render_template, request, make_response
from flask_wtf.csrf import CSRFProtect

from forms import RegistrationForm
from models import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = b'b3374600ed4477da471589f858c5d3183ca2bd753391d4573b93bcb58321d295'
csrf = CSRFProtect(app)

app.conﬁg['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


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
        new_user = User(username=name, usersurname=surname,
                        email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        response = make_response(f'<h1>Вы успешно зарегистрированы!</h1>')
        return response
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
