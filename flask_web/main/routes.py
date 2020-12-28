from flask import render_template
from flask_web import db
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
