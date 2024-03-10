import os

from apiflask import APIFlask
from flask import jsonify, request

from voting.storage import art_storage


def create_app():
  app = APIFlask(__name__)
  return app


app = create_app()


@app.get("/health")
def health_check():
  return 'OK'


@app.get("/art")
def art():
  gen = request.args.get('gen', -1)

  # Return a list of all the requested generation's art metadata.
  return jsonify(art_storage.ArtStorage().get_art(gen))
