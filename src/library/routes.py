from flask import Blueprint, render_template
from flask_login import current_user, login_required, login_user, logout_user

library_bp = Blueprint('library', __name__)


@library_bp.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('library.html', user=current_user)
