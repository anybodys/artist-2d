# Artist 2D Technical Design Doc

status: DRAFT

## Overview

Artest 2D generates abstract 2D art immitating an artist (brush strokes) and making "decisions"
based on "DNA". The better the art, the higher the chance that the DNA will make it to the next
generation.

## Server Architecture


DEPRECATED -- there's now a much simpler one. Haven't updated the diagram yet.

![System Diagram](Artist2d.svg "System Diagram")


## Time Cronjob

1. Close the polls: tally votes and write them to the db.
2. Mix DNA: Mix and match most popular artists' DNA to create the next generation nd write it to the
   db.
3. Paint: Tell the Painting API to paint.

## Painting API

`/paint`: GET.
    1. Get the latest/current generation of DNA from Storage API.
    2. For each new artist, paint their painting.
       * Save image to storage.
    3. Open to polls: Set current generation in Storage API.


## Voting API

`/art`: GET
    1. Read the current generation of art.
    2. Return list of all art for the current generation.

`/heart`: POST
    1. auth user
    2. Record a heart for this artist for this user.

`/heart`: DELETE
    1. auth user
    2. Remove a heart for this artist for this user.


## STORAGE API

`/art`: GET
    1. Read the current generation of art.
    2. Return list of all art for the current generation.


1. Write voting results for a generation.
1. Get DNA, default to current generation.
2. Write DNA.
3. Get art, default to current generation.

## Database

All database tables should have metadata:
```
created_date
updated_date
deleted_date
```

```
Vote:
    id: pk, int
    art: fk
    user: fk
constraint: unique(art, user)

Art:
    id: pk, int
    public_link: varchar (URL)
    generation: fk
    artist: fk

Artist:
    id: pk, int
    dna: varchar
    generation: fk


Generation:
    id: pk, int
    active_date: timestamp, the datetime it went active for hearting.
    inactive_date: timestamp, the datetime it went inactive for hearting.
```
