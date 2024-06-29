import logging

from flask import Flask, jsonify, request
from flask_cors import CORS

from voting import storage as art_storage


def create_app():
  app = Flask(__name__)
  CORS(app)
  app.logger.setLevel(logging.INFO)
  return app


app = create_app()


@app.route("/health")
def health_check():
  return jsonify({'status': 'OK'})


@app.get("/art")
def art():
  gen = request.args.get('gen', 0)

  # Return a list of all the requested generation's art metadata.
  return jsonify(art_storage.get_api().get_art(gen))
