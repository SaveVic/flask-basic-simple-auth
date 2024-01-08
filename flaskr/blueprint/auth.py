from flask import Blueprint, request, redirect, flash, render_template
import flaskr.service.auth as auth_service
import flaskr.service.session as session_service

bp = Blueprint('auth', __name__, url_prefix='/')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if session_service.is_logged_in():
        return redirect('/')
    if request.method == 'POST':
        acc_or_msg = auth_service.login(request.form)
        if not isinstance(acc_or_msg, str):
            session_service.set_session(acc_or_msg)
            return redirect('/')
        flash(acc_or_msg)

    return render_template('login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if session_service.is_logged_in():
        return redirect('/')
    if request.method == 'POST':
        acc_or_msg = auth_service.register(request.form)
        if not isinstance(acc_or_msg, str):
            session_service.set_session(acc_or_msg)
            return redirect('/')
        flash(acc_or_msg)

    return render_template('register.html')


@bp.route('/logout')
def logout():
    session_service.clear_session()
    return redirect('/')
