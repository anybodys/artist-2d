def test_get_health(client):
  response = client.get('/health')
  assert b'OK' == response.data
  assert 200 == response.status_code
