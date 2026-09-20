from datetime import datetime

import pytest

from alarm import add_alarm, is_due, load_alarms, remove_alarm, save_alarms


def test_is_due_exact_match():
    alarm = {"id": 1, "time": "07:30", "label": "wake up"}
    assert is_due(alarm, datetime(2026, 1, 1, 7, 30))


def test_is_due_not_yet():
    alarm = {"id": 1, "time": "07:30", "label": "wake up"}
    assert not is_due(alarm, datetime(2026, 1, 1, 7, 29))


def test_is_due_already_past():
    alarm = {"id": 1, "time": "07:30", "label": "wake up"}
    assert not is_due(alarm, datetime(2026, 1, 1, 8, 0))


def test_add_persists_and_assigns_incrementing_ids(tmp_path):
    path = tmp_path / "alarms.json"
    first_id = add_alarm("07:30", "wake up", path)
    second_id = add_alarm("08:00", "gym", path)
    assert (first_id, second_id) == (1, 2)
    alarms = load_alarms(path)
    assert [a["label"] for a in alarms] == ["wake up", "gym"]


def test_add_rejects_bad_time_format(tmp_path):
    path = tmp_path / "alarms.json"
    with pytest.raises(ValueError):
        add_alarm("7:30am", "wake up", path)


def test_remove_deletes_matching_alarm(tmp_path):
    path = tmp_path / "alarms.json"
    save_alarms([{"id": 1, "time": "07:30", "label": "wake up"}], path)
    assert remove_alarm(1, path) is True
    assert load_alarms(path) == []


def test_remove_returns_false_when_id_missing(tmp_path):
    path = tmp_path / "alarms.json"
    save_alarms([], path)
    assert remove_alarm(99, path) is False


def test_load_alarms_missing_file_returns_empty_list(tmp_path):
    path = tmp_path / "does_not_exist.json"
    assert load_alarms(path) == []
