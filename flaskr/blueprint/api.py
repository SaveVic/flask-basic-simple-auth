from flask import Blueprint, abort
import flaskr.repo.user as rep
import flaskr.service.session as session_service

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/')
def get_all():
    if not session_service.is_logged_in():
        return abort(404)
    accs = rep.get_all()
    s = '</br>'.join([f'Count: {len(accs)}'] + [str(acc) for acc in accs])
    return s
