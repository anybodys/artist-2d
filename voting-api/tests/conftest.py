import pytest

from voting import api

@pytest.fixture()
def app():
  api.app.config.update({
    "TESTING": True,
  })

  # other setup can go here

  yield api.app

  # clean up / reset resources here


@pytest.fixture()
def client(app):
  return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
