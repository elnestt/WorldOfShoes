from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import login_user, get_user_by_id, register_user


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
        user = login_user(email, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!')
            return redirect(url_for('login.profile'))
        else:
            flash('Invalid email or password.')
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