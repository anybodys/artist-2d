# Artist 2D

This is a project for fun that's loosely based on what's probably a totally incorrect interpretation
of a genetic algorithm. Eventually.

This code:
* Programmatically generates abstract art based on input "DNA" files.
* [TODO] Other things like dislays the output for voting, allows voting, mixes the DNA files of vote winners for a new generation, generates the next generation's images, and other such fun behaviors.

## Goals

Some concepts I wanted to include to see how they played out, or because they seemed logical and fun to me:
* Layers of abstraction
   * Just like we don't have chromosome that says "green eyes", these artists don't have chromosomes that say "circle".
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
3. Create a `.env` file that specifies GCP envvars for `/api`.
   - You can start by copying the example and updating the values. `cp .env.example .env`
4. `make setup` will handle pipenv fun for you.
5. Do something to improve this getting started guide!

### Optional setup

1. Run on a virtual display rather than your real display. (Linux)
  - `sudo apt install xvfb`
  - `Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &`
  - In your local `.env` file, add a line `DISPLAY=":99.0"`.
  - Run `make test` to see that you no longer see the display.

## Run

`cd` into either `/client` or `/api` depending which you want to run. To run both for a functional local system, use two tabs and run both the Client and API.


```
make run
```

## Test

`cd` into either `/client` or `/api` depending which you want to test.


```
make test
```

## Deploy

CD deploys for you. Yay!

1. Ensure CI is passing on main.
1. Bump the version in (variables.tf)[infra/app/variables.tf] for the Client or the API depending which you want to deploy.
1. Create a new PR with the version bump.
1. Merge the PR
1. Watch the Infra CD pipeine do its magic! It'll build a new image and update the Cloud Run function.


## Learn More

[Tech Spec](docs/tech_spec.md)
