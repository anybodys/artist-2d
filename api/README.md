# Artist 2D - API

The backend API that the frontend and internal crons use to do things.

## Getting Started

This is a WIP.

### One-time Setup

This only needs to be run once per local development machine, not for each API directory.

1. You will need python (see Pipfile for version) and pip.
2. You will need to set to create a gcp iam role for your local dev (name it "YOURNAME-local-dev") and download the json secret stuff.


### Local Setup

Set up your local development environment for the API.


3. Create a `.env` file that specifies GCP envvars.
   - You can start by copying the example and updating the values. `cp .env.example .env`
   - Or you can copy a `.env` file from another api in this project.
4. `make setup` will handle pipenv fun for you.
5. Do something to improve this getting started guide!

## Run

```
make run
```

## Test

```
make test
```

## Deploy

Bump the version in (variables.tf)[../infra/app/variables.tf] and merge PR. The CD pipeline will test and deploy.

## Learn More

[Tech Spec](docs/tech_spec.md)


## Social Auth

http://localhost:8000/accounts/google/login/?process=login
