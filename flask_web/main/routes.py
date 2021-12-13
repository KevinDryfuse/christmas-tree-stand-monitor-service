from datetime import datetime

from operator import attrgetter

from flask import render_template, request, make_response, jsonify, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import abort

from flask_web import db
from flask_web.enums.Status import Status
from flask_web.main import bp
from flask_web.main.DisplayCard import DisplayCard
from flask_web.main.forms import Login, Register, EditProfile, Add, EditStand
from flask_web.models import User, Stand, StatusHistory, Product


@bp.route("/", methods=["GET"])
@bp.route("/index", methods=["GET"])
@login_required
def index():
    stands = db.session.query(Stand).all()
    dc = DisplayCard()
    return render_template("index.html", title="Dashboard - Christmas Tree Monitoring Service", stands=stands, dc=dc)


@bp.route("/throw", methods=["GET"])
def throw():
    raise Exception("This is an error!")


@bp.route("/stands/<string:external_id>", methods=["GET"])
@login_required
def get_stand(external_id):
    try:
        stand = db.session.query(Stand).filter(Stand.external_id == external_id).one()
    except NoResultFound:
        abort(404)

    response = make_response(jsonify(stand.serialize()), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@bp.route("/stands/<string:external_id>/status", methods=["GET", "POST"])
def stand_status(external_id):
    try:
        stand = db.session.query(Stand).filter(Stand.external_id == external_id).one()
    except NoResultFound:
        abort(404)

    if request.method == "POST":

        try:
            status = Status(request.json.get("status")).value
            print(status)
        except ValueError:
            abort(422, "Status {} is invalid".format(request.json.get("status")))

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


@bp.route("/stands/<string:external_id>/history", methods=["GET"])
def stand_history(external_id):
    try:
        stand = db.session.query(Stand).filter(Stand.external_id == external_id).one()
        stand.history.sort(key=attrgetter('status_date'), reverse=True)
    except NoResultFound:
        abort(404)

    return render_template("history.html", title=f"History - {stand.name}", stand=stand)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("main.login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("main.index"))
    return render_template("login.html", title="Sign In", form=form)


# TODO: Tests
@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


# TODO: Tests
@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = Register()

    if request.method == "POST":
        if form.validate_on_submit():
            if form.validate_email_not_already_registered():
                user = User(email=form.email.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            plaintext_password=form.password.data)
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for("main.index"))
            else:
                flash("Email address has already been registered")

    return render_template("register.html", title="Register", form=form)


# TODO: Tests
@bp.route("/profile", methods=["GET", "POST"])
@login_required
def edit_profile():

    user_id = current_user.id

    u = db.session.query(User).filter(User.id == user_id).one()
    form = EditProfile()

    if request.method == "POST":
        if form.validate_on_submit():
            db.session.query(User).filter(User.id == user_id).update(
                {User.first_name: form.first_name.data,
                 User.last_name: form.last_name.data}, synchronize_session=False)
            db.session.commit()

            return redirect(url_for("main.index"))

    form.first_name.data = u.first_name
    form.last_name.data = u.last_name
    form.email.data = u.email

    return render_template("edit_profile.html", title="Edit Profile", form=form)


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add_stand():

    user_id = current_user.id
    form = Add()

    if request.method == "POST":
        if form.validate_on_submit():

            product = Product.query.filter_by(registration_id=form.registration_id.data.upper()).first()
            if product is None:
                flash("Device Registration ID is not valid, please try again")
                return redirect(url_for("main.add_stand"))
            else:
                s = Stand(user_id=user_id, external_id=product.external_id, registration_id=product.registration_id, name=form.name.data)
                db.session.add(s)
                db.session.commit()

                return redirect(url_for("main.index"))

    return render_template("add.html", title="Add New Stand", form=form)


@bp.route("/manage/<string:external_id>/edit", methods=["GET", "POST"])
@login_required
def edit_stand(external_id):
    print(external_id)
    form = EditStand()

    s = db.session.query(Stand).filter(Stand.external_id == external_id).one()
    form.registration_id.data = s.registration_id
    form.name.data = s.name

    return render_template("edit_stand.html", title="Edit Stand", form=form)


@bp.route("/health", methods=["GET", "POST"])
def health():
    print("HERE!")

    return render_template("health.html", title="Health")
