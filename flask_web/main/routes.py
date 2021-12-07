from datetime import datetime

from flask import render_template, request, make_response, jsonify, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import abort

from flask_web import db
from flask_web.enums.Status import Status
from flask_web.main import bp
from flask_web.main.forms import Login, Register, EditProfile
from flask_web.models import User, Stand, StatusHistory


@bp.route("/", methods=["GET"])
@bp.route("/index", methods=["GET"])
@login_required
def index():
    stands = db.session.query(Stand).all()
    return render_template("index.html", title='Dashboard - Christmas Tree Monitoring Service', stands=stands)


@bp.route("/throw", methods=["GET"])
def throw():
    raise Exception("This is an error!")


@bp.route('/stand/<string:external_id>', methods=["GET"])
@login_required
def get_stand(external_id):
    try:
        stand = db.session.query(Stand).filter(Stand.external_id == external_id).one()
    except NoResultFound:
        abort(404)

    response = make_response(jsonify(stand.serialize()), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@bp.route('/stand/<string:external_id>/status', methods=["GET", "POST"])
@login_required
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


# TODO: Tests
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Sign In', form=form)


# TODO: Tests
@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


# TODO: Tests
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = Register()

    if request.method == 'POST':
        if form.validate_on_submit():
            if form.validate_email_not_already_registered():
                user = User(email=form.email.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            plaintext_password=form.password.data)
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('main.index'))
            else:
                flash('Email address has already been registered')

    return render_template('register.html', title='Register', form=form)


# TODO: Tests
@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    u = db.session.query(User).filter(User.id == current_user.id).one()
    print(u)
    form = EditProfile()

    form.first_name.data = u.first_name
    form.last_name.data = u.last_name
    form.email.data = u.email

    if request.method == 'POST':
        if form.validate_on_submit():
            print("XXXXX")

    return render_template("edit_profile.html", title='Edit Profile', form=form)
