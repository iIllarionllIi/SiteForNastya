from flask import Flask, render_template, request, session, g, redirect, url_for, flash
from flask_babel import Babel
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env файла
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['BABEL_DEFAULT_LOCALE'] = 'ru'

# Конфигурация для отправки email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'lillarionllil@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')  # Пароль нужно будет установить через переменную окружения
app.config['MAIL_DEFAULT_SENDER'] = 'lillarionllil@gmail.com'

babel = Babel(app)
mail = Mail(app)

# Поддерживаемые языки
LANGUAGES = {
    'en': 'English',
    'ru': 'Русский'
}

# Захешированный пароль (1324)
ADMIN_PASSWORD_HASH = generate_password_hash('1324')

# Декоратор для защиты админ-маршрутов
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def get_locale():
    if 'lang_code' in session:
        return session['lang_code']
    return request.accept_languages.best_match(LANGUAGES.keys())

babel.init_app(app, locale_selector=get_locale)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message_text = request.form.get('message')
        
        try:
            # Создаем сообщение
            msg = Message(
                subject=f'Новое сообщение от {name}',
                recipients=['lillarionllil@gmail.com'],
                body=f'''
                Новое сообщение с сайта:
                
                От: {name}
                Email: {email}
                
                Сообщение:
                {message_text}
                '''
            )
            # Отправляем email
            mail.send(msg)
            flash('Спасибо! Ваше сообщение успешно отправлено.', 'success')
        except Exception as e:
            flash('Извините, произошла ошибка при отправке сообщения. Пожалуйста, попробуйте позже.', 'error')
            print(f"Error sending email: {e}")
        
        return redirect(url_for('contacts'))
    
    return render_template('contacts.html')

@app.route('/set_language/<language>')
def set_language(language):
    session['lang_code'] = language
    return redirect(request.referrer or '/')

# Админ-маршруты
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if check_password_hash(ADMIN_PASSWORD_HASH, password):
            session['is_admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin/login.html', error='Неверный пароль')
    return render_template('admin/login.html')

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    # Здесь можно добавить загрузку текущего контента
    about_text = "Текущий текст 'Обо мне'"
    services = [
        {'name': 'Услуга 1', 'price': '5000 ₽', 'description': 'Описание услуги 1'},
        {'name': 'Услуга 2', 'price': '8000 ₽', 'description': 'Описание услуги 2'},
        {'name': 'Услуга 3', 'price': '15000 ₽', 'description': 'Описание услуги 3'},
    ]
    return render_template('admin/dashboard.html', about_text=about_text, services=services)

@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    return redirect(url_for('index'))

@app.route('/admin/update_about', methods=['POST'])
@admin_required
def admin_update_about():
    about_text = request.form.get('about_text')
    # Здесь можно добавить сохранение текста
    flash('Текст "Обо мне" успешно обновлен')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/update_services', methods=['POST'])
@admin_required
def admin_update_services():
    # Здесь можно добавить обновление услуг
    flash('Услуги успешно обновлены')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True, port=8007)
