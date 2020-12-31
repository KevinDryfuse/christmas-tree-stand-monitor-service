from datetime import datetime, timedelta

from flask_web.enums.Status import Status
from flask_web.models import Stand, StatusHistory


def test_new_stand():
    """
    GIVEN a Stand model
    WHEN a new Stand is created
    THEN check the properties are defined correctly
    """

    # Setup stand
    today = datetime.now()
    stand = Stand(name="Example Stand", current_date=today)

    # Validate stand information
    assert stand.status == 'low'
    assert stand.history == []
    assert stand.status_date == today
    assert len(stand.external_id) == 36
    assert len(stand.registration_id) == 10


def test_add_history():
    """
    GIVEN a Stand model
    WHEN history is added to the stand
    THEN check the history is created correctly
    """

    # Setup stand
    today = datetime.now()
    stand = Stand(name="Example Stand", current_date=today)

    # Add history
    stand.add_history(status=Status.full.value, status_date=(today - timedelta(days=1)))
    stand.add_history(status=Status.acceptable.value, status_date=(today - timedelta(days=2)))

    # Validate history information
    assert stand.history[0].status == Status.full.value
    assert stand.history[0].status_date == (today - timedelta(days=1))
    assert stand.history[1].status == Status.acceptable.value
    assert stand.history[1].status_date == (today - timedelta(days=2))


def test_stand_serialize():
    """
    GIVEN a Stand object
    WHEN the 'serialize' method is called
    THEN a json object representing the stand is returned
    """

    # Setup stand
    today = datetime.now()
    stand = Stand(name="Example Stand", current_date=today)
    stand.add_history(status=Status.full.value, status_date=(today - timedelta(days=1)))
    stand.add_history(status=Status.acceptable.value, status_date=(today - timedelta(days=2)))

    # Serialize
    result = stand.serialize()

    # Validate json output
    assert result['status'] == Status.low.value
    assert result['name'] == "Example Stand"
    assert result['status_date'] == today.strftime("%Y-%m-%d %H:%M:%S")
    assert result['history'][0]['status'] == Status.full.value
    assert result['history'][0]['status_date'] == (today - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    assert result['history'][1]['status'] == Status.acceptable.value
    assert result['history'][1]['status_date'] == (today - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")


def test_history_serialize():
    """
    GIVEN a StatusHistory object
    WHEN the 'serialize' method is called
    THEN a json object representing the history is returned
    """

    # Setup history
    today = datetime.now()
    history = StatusHistory(stand_id=99, status=Status.full.value, status_date=today)

    # Serialize
    result = history.serialize()

    # Validate json output
    assert result['status'] == Status.full.value
    assert result['status_date'] == today.strftime("%Y-%m-%d %H:%M:%S")
