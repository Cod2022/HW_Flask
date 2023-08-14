# Создать страницу, на которой будет форма для ввода имени и электронной почты, при отправке которой 
# будет создан cookie-файл с данными пользователя, а также будет произведено перенаправление 
# на страницу приветствия, где будет отображаться имя пользователя.
# На странице приветствия должна быть кнопка «Выйти», при нажатии на которую будет удалён 
# cookie-файл с данными пользователя и произведено перенаправление на страницу ввода имени 
# и электронной почты.

from flask import Flask, request, make_response, render_template

app = Flask(__name__)

@app.route('/')
def exit_page():
    return render_template('form.html')

@app.get('/')
def submit_get():
    return render_template('form.html')

@app.post('/hello')
def submit_post():
    name = request.form.get('name')
    email = request.form.get('email')
    response = make_response(render_template('hello.html', name=name, email=email))
    response.set_cookie(name, email)
    return response






if __name__ == '__main__':
    app.run(debug=True)
