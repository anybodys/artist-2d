def test_get_health(client):
  response = client.get('/health')
  assert 'OK' == response.json['status']
  assert 200 == response.status_code
