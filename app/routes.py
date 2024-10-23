from flask import render_template, flash, redirect, url_for, current_app
from app import app
from app.forms import LoginForm, TableForm, RegistrationForm
from app.audit.script import handle_form_submission


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
    data = []

    if form.validate_on_submit():
        table_name = form.table_to_display.data
        
        if table_name == 'Criticals':
            data = handle_form_submission('app/audit/logs/Criticals.txt', 'criticals')
        elif table_name == 'Error':
            data = handle_form_submission('app/audit/logs/Errors.txt', 'error')
        elif table_name == 'Warning':
            data = handle_form_submission('app/audit/logs/Warnings.txt', 'warning')
        
        # Логирование выбранной таблицы и полученных данных
        current_app.logger.info(f"Selected table: {table_name}")
        current_app.logger.info(f"Received data: {data[:5]}...")  # Выводим первые 5 элементов
        
        return render_template('table.html', title='Показать таблицу', form=form, data=data)
    
    # Если форма не была отправлена или не прошла валидацию
    return render_template('table.html', title='Показать таблицу', form=form, data=[])

@app.route('/register')
def register():
    form = RegistrationForm()
    
    return render_template('register.html', title='Sign In', form=form)