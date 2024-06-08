# Artist 2D - Storage API

This is the API that interacts with the database.

## Getting Started

This is a WIP.

### One-time Setup

This only needs to be run once per local development machine, not for each API directory.

1. You will need python (see Pipfile for version) and pip.
2. You will need to set to create a gcp iam role for your local dev (name it "YOURNAME-local-dev") and download the json secret stuff.


### Local Setup

Set up your local development environment for the Storage API.


3. Create a `.env` file that specifies GCP envvars.
   - You can start by copying the example and updating the values. `cp .env.example .env`
   - Or you can copy a `.env` file from another api in this project.
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

## Deploy


```
make deploy
```


## Learn More

[Tech Spec](docs/tech_spec.md)
