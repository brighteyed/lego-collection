from unittest.mock import patch

import pytest

from lego_collection.api import get_set_lists, get_user_token, get_list_sets


def test_get_user_token_success():
    mock_response_data = {"user_token": "abc123"}
    with patch("lego_collection.api.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response_data
        token = get_user_token("key1", "user1", "pass1")
    assert token == "abc123"
    mock_post.assert_called_once_with(
        "https://rebrickable.com/api/v3/users/_token/",
        headers={"Authorization": "key key1"},
        data={"username": "user1", "password": "pass1"},
        timeout=30,
    )


def test_get_user_token_failure():
    with patch("lego_collection.api.requests.post") as mock_post:
        mock_post.return_value.status_code = 401
        with pytest.raises(RuntimeError, match="Authentication failed"):
            get_user_token("key1", "user1", "pass1")


def test_get_set_lists_single_page():
    mock_data = {
        "count": 2,
        "next": None,
        "previous": None,
        "results": [{"id": 100, "name": "My Sets"}, {"id": 101, "name": "Wishlist"}],
    }
    with patch("lego_collection.api.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_data
        lists = get_set_lists("token1", "key1")
    assert len(lists) == 2
    assert lists[0]["id"] == 100
    mock_get.assert_called_once()


def test_get_set_lists_pagination():
    page1 = {
        "next": "https://rebrickable.com/api/v3/users/token1/setlists/?page=2",
        "results": [{"id": 100, "name": "My Sets"}],
    }
    page2 = {"next": None, "results": [{"id": 101, "name": "Wishlist"}]}
    with patch("lego_collection.api.requests.get") as mock_get:
        mock_get.side_effect = [
            type("Resp", (), {"status_code": 200, "json": lambda self=page1: page1})(),
            type("Resp", (), {"status_code": 200, "json": lambda self=page2: page2})(),
        ]
        lists = get_set_lists("token1", "key1")
    assert len(lists) == 2
    assert mock_get.call_count == 2


def test_get_list_sets():
    mock_data = {
        "next": None,
        "results": [
            {"list_id": 100, "set": {"set_num": "10193-1"}, "quantity": 1},
            {"list_id": 100, "set": {"set_num": "10243-1"}, "quantity": 2},
        ],
    }
    with patch("lego_collection.api.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_data
        sets = get_list_sets("token1", 100, "key1")
    assert len(sets) == 2
    assert sets[0]["set"]["set_num"] == "10193-1"