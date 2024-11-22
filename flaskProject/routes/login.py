from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import login_user, get_user_by_id, register_user, get_db_connection
from werkzeug.security import check_password_hash


login_bp = Blueprint('login', __name__)


@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        result = register_user(username, email, password)
        if result == "Registration is successful!":
            flash(result)
            user = login_user(username, password)
            if user:
                session['user_id'] = user['id']
                session['username'] = user['username']
            return redirect(url_for('login.profile'))
        else:
            flash(result)
            return redirect(url_for('login.register'))
    return render_template('register.html')



@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Отримання інформації про користувача за email
        user = cursor.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['email'] = user['email']
            is_admin = bool(user['is_admin'])  # Перевірка статусу адміністратора
            
            # Встановлення додаткових прав, якщо користувач — адміністратор
            if is_admin:
                session['is_admin'] = True
                flash("Ви увійшли як адміністратор")
            else:
                session['is_admin'] = False
                flash("Ви увійшли як звичайний користувач")
            
            conn.close()
            return redirect(url_for('login.profile'))  # Перехід до сторінки акаунта
            
        else:
            flash("Логін або пароль невірний")
            conn.close()
    return render_template('login.html')
    



@login_bp.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login.login'))
    user = get_user_by_id(session['user_id'])
    return render_template('profile.html', user=user)

@login_bp.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!")
    return redirect(url_for('login.login'))