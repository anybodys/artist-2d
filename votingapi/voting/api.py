from flask import Flask, jsonify, request
from flask_cors import CORS

from voting.storage import art_storage, db


def create_app():
  app = Flask(__name__)
  CORS(app)
  return app


app = create_app()


@app.route("/health")
def health_check():
  return jsonify({'status': 'OK'})


@app.get("/art")
def art():
  gen = request.args.get('gen', -1)
  if gen < 0:
    gen = db.get_current_generation()

  # Return a list of all the requested generation's art metadata.
  return jsonify(art_storage.ArtStorage().get_art(gen))
