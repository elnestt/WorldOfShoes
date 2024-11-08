from flask import Blueprint, render_template, url_for
from models import get_db_connection, get_orders, get_order_details, get_products


admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin():
    conect = get_db_connection()
    feedback = conect.execute('SELECT * FROM feedback').fetchall()
    conect.close()
    orders = get_orders()
    return render_template('admin.html', orders=orders, feedback=feedback)