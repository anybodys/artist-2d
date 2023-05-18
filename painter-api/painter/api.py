import os

from flask import Flask, request

from painter import painter
from painter import datastore
from painter.graphics import engine
from painter.storage import art_storage


app = Flask(__name__)


@app.route("/health")
def health_check():
  return 'OK'


@app.route("/paint")
def paint():
  gen = request.args.get('gen', -1)

  # TODO(kmd): This should be processed async.
  graphics_engine = engine.TurtleEngine(art_storage.ArtStorage())
  DS = datastore.Client()
  for artist_id, dna_str in DS.read_dna(gen):
    app.logger.info(f'Artist {artist_id} starting to paint...')
    graphics_engine.reset()
    p = painter.Painter(dna_str, graphics_engine)
    while p.still_growing():
      p.paint()
      p.age_up()
    graphics_engine.save_image(gen, artist_id)
  return 'OK'


if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
