from flask import render_template, request, make_response, jsonify
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import abort

from flask_web import db
from datetime import datetime
from flask_web.enums.Status import Status
from flask_web.main import bp
from flask_web.models import Stand, StatusHistory


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
    try:
        stand = db.session.query(Stand).filter(Stand.external_id == external_id).one()
    except NoResultFound:
        abort(404)

    response = make_response(jsonify(stand.serialize()), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@bp.route('/stand/<string:external_id>/status', methods=["GET", "POST"])
def stand_status(external_id):
    try:
        stand = db.session.query(Stand).filter(Stand.external_id == external_id).one()
    except NoResultFound:
        abort(404)

    if request.method == 'POST':

        try:
            status = Status(request.json.get('status')).value
        except ValueError:
            abort(422, "Status {} is invalid".format(request.json.get('status')))

        status_date = datetime.now()
        status_history = StatusHistory(stand_id=stand.id, status=status, status_date=status_date)
        db.session.query(Stand).filter(Stand.external_id == external_id).update(
            {Stand.status: status, Stand.status_date: status_date},
            synchronize_session=False)
        db.session.add(status_history)
        db.session.commit()
        stand = db.session.query(Stand).filter(Stand.external_id == external_id).one()

    response = make_response(jsonify(stand.status), 200)
    response.headers["Content-Type"] = "application/json"
    return response
