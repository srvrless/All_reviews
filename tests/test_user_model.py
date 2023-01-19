def test_model(user):
    assert user.username == 'neverless'


def test_user_login(user, testapp):
    res = testapp.post('/login', json={'email_address': user.email_address,
                                      'password': user.password_hash})
    assert res.status_code == 200
    assert res.get_json().get('access_token')
