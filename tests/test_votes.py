import pytest
from app.models.votes_model import VoteModel


@pytest.fixture(name="test_vote")
def test_vote(test_posts, session, test_user):
    new_vote = VoteModel(user_id=test_user["id"], post_id=test_posts[3].id)
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/votes", json={"post_id": test_posts[3].id, "dir": 1})

    assert res.status_code == 201


def test_vote_non_existing_post(authorized_client):
    res = authorized_client.post("/votes", json={"post_id": 666, "dir": 1})

    assert res.status_code == 404


def test_vote_unauthorized_user(client, test_posts):
    res = client.post("/votes", json={"post_id": test_posts[3].id, "dir": 1})

    assert res.status_code == 401


def test_vote_twice_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/votes", json={"post_id": test_posts[3].id, "dir": 1})

    assert res.status_code == 409


def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/votes", json={"post_id": test_posts[3].id, "dir": 0})

    assert res.status_code == 204


def test_delete_non_existing_vote(authorized_client, test_posts):
    res = authorized_client.post("/votes", json={"post_id": test_posts[3].id, "dir": 0})

    assert res.status_code == 404
