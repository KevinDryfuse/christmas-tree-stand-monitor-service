import json
from datetime import datetime, timedelta
from flask_web import db
from flask_web.enums.Status import Status
from flask_web.models import Stand, StatusHistory


def test_home_page(test_client, init_database):
    """
    GIVEN a user visits the home page
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid and contains an expected stand record
    """

    # Insert stand information
    current_date = datetime.now()
    stand = Stand(name="This is my stand name!", current_date=current_date)
    db.session.add(stand)
    db.session.commit()

    # validate stand information is in the response
    response = test_client.get('/')
    assert response.status_code == 200
    assert str.encode("This is my stand name! - low - {}".format(current_date)) in response.data


def test_post_status_using_valid_status_type_status_is_changed(test_client, init_database):
    """
    GIVEN a user attempts to update a stand's status
    WHEN a POST is made with a valid status code to the status endpoint '/stand/<string:external_id>/status'
    THEN check that the response is valid and the database has been updated correctly
    """

    # Insert stand information
    current_date = datetime.now()
    stand = Stand(name="This is the stand we are changing!", current_date=current_date)
    db.session.add(stand)
    stand2 = Stand(name="This is the stand we are NOT changing!", current_date=current_date)
    db.session.add(stand2)
    db.session.commit()

    url = "/stand/{}/status".format(stand.external_id)
    # validate stand information is in the response
    response = test_client.post(url, data=json.dumps({'status': 'acceptable'}), headers={'Content-Type': 'application/json'})
    assert response.status_code == 200
    stand_after_changes = db.session.query(Stand).filter(Stand.external_id == stand.external_id).one()
    stand2_after_changes = db.session.query(Stand).filter(Stand.external_id == stand2.external_id).one()
    assert stand_after_changes.status == Status.acceptable.value
    assert stand_after_changes.status_date != current_date
    assert len(stand_after_changes.history) == 1
    assert stand_after_changes.history[0].status == Status.acceptable.value
    assert stand2_after_changes.status == Status.low.value
    assert stand2_after_changes.status_date == current_date
    assert len(stand2_after_changes.history) == 0


def test_post_status_using_invalid_status_type_status_is_not_changed(test_client, init_database):
    """
    GIVEN a user attempts to update a stand's status
    WHEN a POST is made with an invalid valid status code to the status enpoint '/stand/<string:external_id>/status'
    THEN check that the response is 422 and the database has not been updated
    """

    # Insert stand information
    current_date = datetime.now()
    stand = Stand(name="This is the stand we are changing!", current_date=current_date)
    db.session.add(stand)
    stand2 = Stand(name="This is the stand we are NOT changing!", current_date=current_date)
    db.session.add(stand2)
    db.session.commit()

    url = "/stand/{}/status".format(stand.external_id)
    # validate stand information is in the response
    response = test_client.post(url, data=json.dumps({'status': 'SOMETHING STRANGE'}), headers={'Content-Type': 'application/json'})
    assert response.status_code == 422
    stand_after_changes = db.session.query(Stand).filter(Stand.external_id == stand.external_id).one()
    assert stand_after_changes.status == Status.low.value
    assert stand_after_changes.status_date == current_date
    assert len(stand_after_changes.history) == 0


def test_get_status_using_valid_id_status_is_returned(test_client, init_database):
    """
    GIVEN a user visits the status endpoint
    WHEN the '/stand/<string:external_id>/status' endpoint is requested (GET) with an valid external id
    THEN check that the response is valid and contains the expected status
    """

    # Insert stand information
    current_date = datetime.now()
    stand = Stand(name="This is the stand we are viewing!", current_date=current_date)
    stand.status = Status.full.value
    db.session.add(stand)
    db.session.commit()

    url = "/stand/{}/status".format(stand.external_id)
    # validate stand information is in the response
    response = test_client.get(url, headers={'Content-Type': 'application/json'})
    assert response.status_code == 200
    assert json.loads(response.data) == stand.status


def test_get_status_using_invalid_id_404_is_returned(test_client, init_database):
    """
    GIVEN a user visits the status endpoint
    WHEN the '/stand/<string:external_id>/status' endpoint is requested (GET) with an invalid external id
    THEN check that the response is 404
    """
    url = "/stand/{}/status".format("somerandominvalidvalue")
    # validate a 404 is returned
    response = test_client.get(url, headers={'Content-Type': 'application/json'})
    assert response.status_code == 404


def test_get_stand_using_valid_id_stand_is_returned(test_client, init_database):
    """
    GIVEN a user visits the stand endpoint
    WHEN the '/stand/<string:external_id>' endpoint is requested (GET) with an valid external id
    THEN check that the response is valid and contains the expected stand information
    """

    # Insert stand information
    current_date = datetime.now()
    stand = Stand(name="This is the stand we are viewing!", current_date=current_date)
    stand.status = Status.full.value
    stand.add_history(status=Status.low.value, status_date=current_date - timedelta(days=1))
    stand.add_history(status=Status.acceptable.value, status_date=current_date - timedelta(days=2))
    db.session.add(stand)
    db.session.commit()

    url = "/stand/{}".format(stand.external_id)
    # validate stand information is in the response
    response = test_client.get(url, headers={'Content-Type': 'application/json'})
    assert response.status_code == 200
    response_dict = json.loads(response.data)
    assert len(response_dict['history']) == 2
    assert response_dict['status'] == Status.full.value
    assert response_dict['name'] == "This is the stand we are viewing!"
    assert response_dict['status_date'] == current_date.strftime("%Y-%m-%d %H:%M:%S")
    assert response_dict['history'][0]['status'] == Status.low.value
    assert response_dict['history'][0]['status_date'] == (current_date - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    assert response_dict['history'][1]['status'] == Status.acceptable.value
    assert response_dict['history'][1]['status_date'] == (current_date - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")


def test_get_stand_using_invalid_id_404_is_returned(test_client, init_database):
    """
    GIVEN a user visits the stand endpoint
    WHEN the '/stand/<string:external_id>' endpoint is requested (GET) with an invalid external id
    THEN check that the response is 404
    """

    url = "/stand/{}".format("somerandominvalidvalue")

    # validate a 404 is returned
    response = test_client.get(url, headers={'Content-Type': 'application/json'})
    assert response.status_code == 404
