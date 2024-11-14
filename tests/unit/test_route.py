def test_invalid_route(client):
    response = client.get('/invalid_route')
    assert response.status_code == 404