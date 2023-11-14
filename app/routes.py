from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
#эта ф-я будет выполнена перед каждой ф-ей просмотра

@app.route("/")
@app.route("/index")

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
            return redirect ("login")
        elif not user.check_password(form.password.data):
            flash("Invalid password")
            return redirect ("login")
        login_user(user, remember = form.remember_me.data)
        print(request.args)
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


@app.route("/user/<username>")
@login_required #ф-я может быть просмотрена только авторизированными пользователями
def user(username):
    #если пользователь в системе - перенаправит на главную
    #if current_user.is_authenticated:
    #   return redirect (url_for('index'))
    user = User.query.filter_by(username = username).first_or_404()
    posts = [
        {
            'author' : user,
            'body':'Test post #1'
        },
        {
            'author' : user,
            'body':'Test post #2'
        }
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved")
        return redirect(url_for('user', username = current_user.username))
    elif request.method == 'GET':
        current_user.username = current_user.username 
        current_user.about_me = current_user.about_me 
    return render_template("edit_profile.html", title = "Edit Profile", form=form)