from flask import Blueprint, render_template, url_for, redirect, request, session, flash
from models import get_db_connection, get_orders, get_order_details, update_order_status, delete_order


admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin():
    if session.get('is_admin') is not True:  # Перевірка, чи є в сесії ключ is_admin
        flash('У вас немає прав адміна')
        return redirect(url_for('base'))
    conect = get_db_connection()
    feedback = conect.execute('SELECT * FROM feedback').fetchall()
    users = conect.execute('SELECT * FROM users').fetchall()
    conect.close()
    orders = get_orders()
    return render_template('admin.html', orders=orders, feedback=feedback, users=users)


@admin_bp.route('/admin/delete_feedback/<int:id>', methods=['POST'])
def delete_feedback(id):
    if session.get('is_admin') is not True:  # Перевірка, чи є в сесії ключ is_admin
        flash('У вас немає прав адміна')
        return redirect(url_for('base'))
    conn = get_db_connection()
    conn.execute('DELETE FROM feedback WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/order/<int:order_id>')
def details(order_id):
    if session.get('is_admin') is not True:  # Перевірка, чи є в сесії ключ is_admin
        flash('У вас немає прав адміна')
        return redirect(url_for('base'))
    order, items = get_order_details(order_id)
    return render_template('details.html', order=order, items=items)


@admin_bp.route('/admin/update_order_status/<int:order_id>', methods=['POST'])
def update_order(order_id):
    if session.get('is_admin') is not True:  # Перевірка, чи є в сесії ключ is_admin
        flash('У вас немає прав адміна')
        return redirect(url_for('base'))
    status = request.form['status']
    update_order_status(order_id, status)
    return redirect(url_for('admin.admin'))


@admin_bp.route('/admin/delete_order/<int:order_id>', methods=['POST'])
def delete_order_route(order_id):
    if session.get('is_admin') is not True:  # Перевірка, чи є в сесії ключ is_admin
        flash('У вас немає прав адміна')
        return redirect(url_for('base'))
    delete_order(order_id)
    return redirect(url_for('admin.admin'))

