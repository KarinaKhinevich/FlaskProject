from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route("/")
@app.route("/index")
def index():
    users = {"username":"Miguel"}
    posts = [
        {
            'author' : {'username': 'John'},
            'body':'Beautiful day in Portland'
        },
        {
            'author' : {'username': 'Susan'},
            'body':'I love coding'
        },
        {
            'author' : {'username': 'Grinch'},
            'body':"I'm going to steal ur Xmas"
        }


    ]
    return render_template("index.html", title = "Home", users=users, posts = posts)
    
@app.route('/login', methods = ['GET', "POST"]) 
#по умолчанию methods только GET
#GET  возвращают инфу клиенту(браузеру), 
#POST ипользуются когда браузер отдает инфу 
#ошибка "Method Not Allowed" появляется потому что браузер пытался 
#передать запрос POST, а приложение не настроено на его принятие
def login():
    form = LoginForm() 
    #form.validate_on_submit выполянет обработку формы, 
    #когда браузер отправляет GET запрос, то метод возвращает False
    #когда браузер отправляет POST запрос после нажатия кнопки sibmit
    #метод собирает все данные, запускает валидаторы и если все ок - вренет True
    if form.validate_on_submit(): 
        #flash отправляет пользователю сообшение, но не опказывает автоматически
        flash(f"Login requested for user {form.username.data}, remember_me={form.remember_me.data}")
        #redirect автоматически перенаправляет по другому адресу
        #url_for() гененрирует URL адрес для указанной ф-и представления
        return redirect(url_for('index') )
    return render_template('login.html', title = "Sign In", form = form)

