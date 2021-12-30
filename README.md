# Artist 2D

This is a project for fun that's loosely based on what's probably a totally incorrect interpretation
of a genetic algorithm. Eventually.

This code:
* Programmatically generates abstract art based on input "DNA" files.
* [TODO] Other things like dislays the output for voting, allows voting, mixes the DNA files of vote winners for a new generation, generates the next generation's images, and other such fun behaviors.

## Goals

Some concepts I wanted to include to see how they played out, or because they seemed logical and fun to me:
* Layers of abstraction
   * Just like we don't have chromosome that says "green eyes", these artists don't hae chromosomes that say "circle".
   * I chose to use ATCG as my initial input even though I could have used any sort of abstraction.
 * Semantic meaning
   * Every cell in our body has the same DNA. So why is a skin cell so different than a brain cell? Semantic meaning! I think.
   * The expressions of a gene should be relative to the existing context. I define "read" operations as "semantic inputs", i.e., I read the current state of the world (turtle) to determine the arguments to the actions (move, set color, etc).
 * Free
   * I'm cheap. Architectural decisions are based both on need and cost. Strong emphasis on cost.
 * Fun
   * I've been kicking this idea around my head since grad school. (2007. Yeah, just one year. Because I left after that.)
   * I do leadership roles now for work. I dearly miss python. It's just such an awesome language for mucking around like this.

## Getting Started

This is a WIP.

1. You will need python (see Pipfile for version) and pip.
2. You will need to set to create a gcp iam role for your local dev (name it "YOURNAME-local-dev") and download the json secret stuff.
3. Create a `.env` file that specifies GCP envvars. TODO(kmd): add `example.env` for folks to start from.
4. `make setup` will handle pipenv fun for you.
5. Do something to improve this getting started guide!

## Run

```
make run
```

This generate and an image to a path I find convenient because I haven't made it a variable yet.

## Test

```
make test
```

TODO: CI

## Deploy

Nothing to deploy yet. :)
