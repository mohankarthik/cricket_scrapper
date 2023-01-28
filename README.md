# Cricket Data Scrapping

## Installation

### Python and dependencies

- Install python 3
- Create a venv `python3 -m venv venv`
- Activate the venv
  - Windows: `./venv/bin/activate`
  - \*nix: `. ./venv/bin/activate`
- Update pip if needed `pip3 install --upgrade pip`
- Install dependencies `pip3 install -r requirements.txt`

### MongoDB

- Either
  1. Directly install [MongoDB](https://www.mongodb.com/try/download/community) (or)
  2. Install via [docker](https://www.docker.com/products/docker-desktop/) and then `docker compose up -d`
- Install [Mongo Compass](https://www.mongodb.com/products/compass)
- Update `.env` files based on your local mongo configuration (only if any changes are needed)

## Running

`python3 update.py`

- It'll check the BCCI webpage for all currently running competitions
- It'll then check the existing MongoDB database for matches in those competions that are already saved
- It'll then go back to BCCI webpage and get all new matches and save them to the database

## DB Operations

Open MongoDB compose, navigate to the collection

### Backup

- Click on `Export Collection`, and save the file.
- This file can be used to move the collection data to a different database in the future

### Query

- [Tutorial](https://www.mongodb.com/docs/manual/tutorial/query-documents/)
