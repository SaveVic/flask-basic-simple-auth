from flask import Blueprint, abort, g, render_template
import flaskr.repo.user as rep
import flaskr.service.session as session_service

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/')
def get_all():
    if not session_service.is_logged_in():
        return abort(404)
    users = rep.get_all()
    g.users = users
    # s = '</br>'.join([f'Count: {len(users)}'] + [str(user) for user in users])
    # return s
    return render_template('api.html')
