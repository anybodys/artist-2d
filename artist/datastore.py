import zlib

from google.cloud import datastore


class Client:

  def __init__(self):
    self.client = datastore.Client(namespace='artist2d')
    self.key_dna_generations = self.client.key('entity', 'dna', 'entity', 'generation')

  def read_dna(self, generation):
    """Generator for all the DNA records for single generation."""
    key_gen = self._get_dna_generation_key(generation)
    #dna_array = datastore.Entity(key_gen)
    dna_array = self.client.get(key_gen)
    for artist_id, artist_dna in dna_array.items():
      dna_blob = artist_dna['encoded_dna']
      raw_dna = zlib.decompress(dna_blob)
      yield artist_id, raw_dna.decode('utf-8')

  def write_new_dna(self, generation, artist_id, raw_dna):
    if hasattr(raw_dna, 'encode'):
      # If this is a string, convert to bytes.
      raw_dna = raw_dna.encode()

    gen_key = self._get_dna_generation_key(generation)
    artists_dna = self.client.get(gen_key)
    if not artists_dna:
      print(f'Staring new generation {generation} in firestore')
      artists_dna = datastore.Entity(gen_key)

    encoded_dna = zlib.compress(raw_dna)
    artists_dna.update({str(artist_id): {'encoded_dna': encoded_dna}})
    self.client.put(artists_dna)

  def _get_dna_generation_key(self, generation):
    return self.client.key(
      'entity', str(generation), 'entity', 'artists', parent=self.key_dna_generations)
