import random
import uuid

from artist import datastore

# Quick script to bootstrap gen 0.

NUM_ARTISTS = 32

NUM_CHROMOSOMES = 16

MIN_CHROMOSOME_LENGTH = 128
MAX_CHROMOSOME_LENGTH = 256

firebase = datastore.Client()

for i in range(NUM_ARTISTS):
  artist_id = uuid.uuid4()
  chromosomes = []
  for j in range(NUM_CHROMOSOMES):
    # This is inclusive. We want exclusive max.
    chromo_len = random.randint(MIN_CHROMOSOME_LENGTH, MAX_CHROMOSOME_LENGTH-1)
    chromo_str = ''.join(random.choices('ATCG', k=chromo_len))
    chromosomes.append(chromo_str)
  # Now we have all the chromosomes for one artist.
  raw_dna = '\n'.join(chromosomes)
  print(raw_dna)
  print('--------')
  firebase.write_new_dna(0, artist_id, raw_dna)
