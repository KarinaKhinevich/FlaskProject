from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

@app.route("/")
@app.route("/index")
@login_required #ф-я может быть просмотрена только авторизированными пользователями

def index():
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
    return render_template("index.html", title = "Home",  posts = posts)
    
@app.route('/login', methods = ['GET', "POST"]) 
#по умолчанию methods только GET,GET  возвращают инфу клиенту(браузеру), POST ипользуются когда браузер отдает инфу ошибка "Method Not Allowed" появляется потому что браузер пытался передать запрос POST, а приложение не настроено на его принятие
def login():
    #если пользователь в системе - перенаправит на главную
    if current_user.is_authenticated:
        return redirect (url_for('index'))
    form = LoginForm() 

    #form.validate_on_submit выполянет обработку формы, когда браузер отправляет GET запрос, то метод возвращает False,когда браузер отправляет POST запрос после нажатия кнопки sibmit метод собирает все данные, запускает валидаторы и если все ок - вренет True
    if form.validate_on_submit(): 

        #flash отправляет пользователю сообшение, но не опказывает автоматически
        ##flash(f"Login requested for user {form.username.data}, remember_me={form.remember_me.data}")
        
        #redirect автоматически перенаправляет по другому адресу
        #url_for() гененрирует URL адрес для указанной ф-и представления
        user = User.query.filter_by(username = form.username.data).first()
        if user is None :
            flash("Invalid username")
            return redirect (url_for('login'))
        elif not user.check_password(form.password.data):
            flash("Invalid password")
            return redirect (url_for('login'))
        login_user(user, remember = form.remember_me.data)
        next_page = request.args.get('next') # берем значение next из словоря с полным URL, чтобы определить предыдушую страницу для перенаправления, в случаее если не было доступа для неавторизированного пользователя
        if not next_page or url_parse(next_page).netloc != "": #проверка что next  параметра нет, или что в качестве next параметра задается сторонний сайт (url_parse(next_page).netloc проверяет на наличие полного URL адреса,включающего домен)
             next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title = "Sign In", form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods = ["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit(): 
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations! You are in system now!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)
