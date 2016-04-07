from flask import url_for


def test_base(client):
    response = client.get(url_for('hello'))
    assert response.status_code == 200
    assert 'moi' in response.data.decode('utf-8')


def test_add(db_session, client):
    r = client.get(url_for('add', name='test'))
    r = client.get(url_for('hello'))
    assert r.status_code == 200
    assert 'moi' in r.data.decode('utf-8')
    assert 'test' in r.data.decode('utf-8')


def test_rollback(client):
    response = client.get(url_for('hello'))
    assert response.status_code == 200
    assert 'moi' in response.data.decode('utf-8')
    assert 'test' not in response.data.decode('utf-8')


def test_multiple_add(db_session, client):
    r = client.get(url_for('add', name='test0'))
    r = client.get(url_for('add', name='test1'))
    r = client.get(url_for('hello'))
    assert r.status_code == 200
    assert 'moi' in r.data.decode('utf-8')
    assert 'test0' in r.data.decode('utf-8')
    assert 'test1' in r.data.decode('utf-8')


def test_rollback_after_multiple_add(client):
    response = client.get(url_for('hello'))
    assert response.status_code == 200
    assert 'moi' in response.data.decode('utf-8')
    assert 'test0' not in response.data.decode('utf-8')
    assert 'test1' not in response.data.decode('utf-8')
