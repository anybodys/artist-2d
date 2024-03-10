from pathlib import Path

from apiflask import APIFlask
from flask import jsonify, request

from voting.storage import art_storage


def create_app():
  app = APIFlask(__name__, title='Artist 2D Voting API', spec_path='/openapi.yaml')
  return app


app = create_app()
app.config.update({
  'SPEC_FORMAT': 'yaml',
  'OPENAPI_VERSION': '2.0',
  'SYNC_LOCAL_SPEC': True,
  'LOCAL_SPEC_PATH': Path(app.root_path) / 'openapi.yaml',
})


@app.spec_processor
def google_endpoints_spec(spec):
    spec['host'] = 'gateway-c24bw3cnyq-wl.a.run.app'
    spec['x-google-backend'] = {
      'address': 'voting-api',
      'protocol': 'h2',
    }
    return spec


@app.get("/health")
def health_check():
  return 'OK'


@app.get("/art")
def art():
  gen = request.args.get('gen', -1)

  # Return a list of all the requested generation's art metadata.
  return jsonify(art_storage.ArtStorage().get_art(gen))
