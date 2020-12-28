from flask import render_template, request, make_response, jsonify
from flask_web import db
from datetime import datetime
from flask_web.enums.Status import Status
from flask_web.main import bp
from flask_web.models import Stand


@bp.route("/", methods=["GET"])
@bp.route("/index", methods=["GET"])
def index():
    stands = db.session.query(Stand).all()
    return render_template("index.html", title='Dashboard - Christmas Tree Monitoring Service', stands=stands)


@bp.route("/throw", methods=["GET"])
def throw():
    raise Exception("This is an error!")


@bp.route('/stand/<string:external_id>', methods=["GET"])
def get_stand(external_id):
    stand = db.session.query(Stand).filter(Stand.external_id == external_id).one()
    response = make_response(jsonify(stand.serialize()), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@bp.route('/stand/<string:external_id>/status', methods=["GET", "POST"])
def update_status(external_id):

    if request.method == 'POST':
        status = Status(request.json.get('status')).value
        db.session.query(Stand).filter(Stand.external_id == external_id).update(
            {Stand.status: status, Stand.status_date: datetime.now()},
            synchronize_session=False)
        db.session.commit()

    stand = db.session.query(Stand).filter(Stand.external_id == external_id).one()

    response = make_response(jsonify(stand.status), 200)
    response.headers["Content-Type"] = "application/json"
    return response
