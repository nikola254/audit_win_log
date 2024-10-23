from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, TableForm, RegistrationForm
from app.script import handle_form_submission


@app.route('/')

@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)
        
@app.route('/table', methods=['GET', 'POST'])
def table():
    form = TableForm()
    data = []  # Инициализируйте data как пустой список
    if form.validate_on_submit():
        data = handle_form_submission('app/Criticals.txt')
    return render_template('table.html', title='Показать таблицу', form=form, data=data)

@app.route('/register')
def register():
    form = RegistrationForm()
    
    return render_template('register.html', title='Sign In', form=form)