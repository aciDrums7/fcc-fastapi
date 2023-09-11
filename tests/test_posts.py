import pytest
from app.schemas.posts_schemas import PostOut

# 5 GET


def test_get_all_posts(authorized_client, test_posts, test_user):
    res = authorized_client.get("/posts")
    posts = [PostOut(**post) for post in res.json()]
    print(posts)
    assert len(posts) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts")
    print(res.json())

    assert res.status_code == 401


def test_get_existing_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = PostOut(**res.json())
    print(post)

    assert res.status_code == 200
    assert post.id == test_posts[0].id
    assert post.content == test_posts[0].content
    assert post.title == test_posts[0].title


def test_get_non_existing_post(authorized_client, test_posts):
    res = authorized_client.get("/posts/666")
    print(res.json())

    assert res.status_code == 404


def test_unauthorized_user_get_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    print(res.json())

    assert res.status_code == 401


# 5 POST


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("awesome new title", "awesome new content", True),
        ("favorite pizza", "i love pepperoni", True),
        ("tallest skyscrapers", "gigachad > chuck norris", True),
        ("qui c'è il chico shniff shneff", "come na mortadella", None),
    ],
)
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post(
        "/posts", json={"title": title, "content": content, "published": published}
    )

    created_post = PostOut(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    if published is None:
        assert created_post.published is False
    else:
        assert created_post.published == published
    assert created_post.owner.id == test_user["id"]


def test_unauthorized_user_create_post(client, test_posts):
    res = client.post("/posts")
    print(res.json())

    assert res.status_code == 401


# 5 PUT


def test_update_post(authorized_client, test_user, test_posts):
    payload = {
        "title": "updated title",
        "content": "updated content",
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=payload)
    updated_post = PostOut(**res.json())
    print(updated_post)

    assert res.status_code == 200
    assert updated_post.title == payload["title"]
    assert updated_post.content == payload["content"]


def test_update_other_user_post(authorized_client, test_user, test_posts):
    payload = {
        "title": "updated title",
        "content": "updated content",
    }

    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=payload)
    print(res.json())

    assert res.status_code == 403


def test_unauthorized_user_updates_post(client, test_posts):
    payload = {
        "title": "updated title",
        "content": "updated content",
    }

    res = client.put(f"/posts/{test_posts[3].id}", json=payload)
    print(res.json())

    assert res.status_code == 401


def test_update_non_existing_post(authorized_client, test_user, test_posts):
    payload = {
        "title": "updated title",
        "content": "updated content",
    }

    res = authorized_client.put(f"/posts/666", json=payload)
    print(res.json())

    assert res.status_code == 404


# 5 DELETE


def test_delete_existing_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204


def test_delete_non_existing_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete("/posts/666")
    print(res.json())

    assert res.status_code == 404


def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    print(res.json())

    assert res.status_code == 401


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")

    assert res.status_code == 403
