from flask import render_template, flash, redirect, url_for, current_app, request
from app import app
from app.forms import LoginForm, TableForm, RegistrationForm
from app.audit.script import handle_form_submission, output_all_log_file


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
    table_data = False
    selected_table = False
    images = []  # Список для хранения имен файлов изображений

    if request.method == 'POST':
        if form.validate_on_submit():
            if 'out_all_log' in request.form:
                try:
                    data = output_all_log_file('app/audit/logs/Informations.txt', 'all_log_file')
                    table_data = True
                    selected_table = 'all_log'
                    return render_template('table.html', title='Список всех логов', form=form, data=data, table_data=table_data, selected_table=selected_table, images=images)
                except Exception as e:
                    current_app.logger.error(f"Ошибка при получении данных о всех логах: {str(e)}")
                    flash(f"Ошибка при получении данных о всех логах: {str(e)}", category='error')
                    return redirect(url_for('table'))

            elif 'submit' in request.form:
                table_name = form.table_to_display.data
                
                if table_name == 'Criticals':
                    try:
                        data = handle_form_submission('app/audit/logs/Criticals.txt', 'criticals')
                        table_data = True
                        selected_table = 'criticals'
                        return render_template('table.html', title=f'Таблица {table_name}', form=form, data=data, table_data=table_data, selected_table=selected_table, images=images)
                    except Exception as e:
                        current_app.logger.error(f"Ошибка при обработке таблицы Критичных: {str(e)}")
                        flash(f"Ошибка при обработке таблицы Критичных: {str(e)}", category='error')
                        return redirect(url_for('table'))

                elif table_name == 'Error':
                    try:
                        data = handle_form_submission('app/audit/logs/Errors.txt', 'error')
                        table_data = True
                        selected_table = 'error'
                        return render_template('table.html', title=f'Таблица {table_name}', form=form, data=data, table_data=table_data, selected_table=selected_table, images=images)
                    except Exception as e:
                        current_app.logger.error(f"Ошибка при обработке таблицы Ошибок: {str(e)}")
                        flash(f"Ошибка при обработке таблицы Ошибок: {str(e)}", category='error')
                        return redirect(url_for('table'))

                elif table_name == 'Warning':
                    try:
                        data = handle_form_submission('app/audit/logs/Warnings.txt', 'warning')
                        table_data = True
                        selected_table = 'warning'
                        return render_template('table.html', title=f'Таблица {table_name}', form=form, data=data, table_data=table_data, selected_table=selected_table, images=images)
                    except Exception as e:
                        current_app.logger.error(f"Ошибка при обработке таблицы Предупреждений: {str(e)}")
                        flash(f"Ошибка при обработке таблицы Предупреждений: {str(e)}", category='error')
                        return redirect(url_for('table'))

            elif 'classify' in request.form:  # Обработка нажатия кнопки "Классифицировать"
                try:
                    # Здесь добавьте код для выполнения классификации и сохранения изображений
                    images = [
                                url_for('static', filename='confusion_matrix.png'),
                                url_for('static', filename='feature_importance.png'),
                                url_for('static', filename='decision_tree.png'),
                            ]  # Пример имен файлов изображений
                    # Вы можете добавить логику для генерации изображений на основе ваших данных
                    return render_template('table.html', title='Результаты классификации', form=form, data=data, table_data=table_data, selected_table=selected_table, images=images)
                except Exception as e:
                    current_app.logger.error(f"Ошибка при классификации: {str(e)}")
                    flash(f"Ошибка при классификации: {str(e)}", category='error')
                    return redirect(url_for('table'))

    # Если GET-запрос или форма не была отправлена
    return render_template('table.html', title='Выбор таблицы', form=form, data=[], table_data=False, selected_table=None, images=images)

@app.route('/register')
def register():
    form = RegistrationForm()
    
    return render_template('register.html', title='Sign In', form=form)