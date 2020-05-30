# daylio-stats

A tool to generate stats/charts from Daylio CSV exports.

Currently supports:

- Creating a chart of all data since the beginning of tracking
- Smoothing the chart with a rolling average

Locally you can use:

```
$ ./manage.py generate_charts <path to Daylio CSV>
```

to get more charts than we're able to generate now on Heroku.

## Running locally

### Installation

After cloning the repo:

- `$ npm install`
- `$ pipenv install`

### Secret key for Django

Either set the `DS_SECRET_KEY` env variable directly, or read the key from a file.

For bash:

```bash
$ export DS_SECRET_KEY=$(cat .ds_secret_key)
```

For fish:

```fish
$ set -x DS_SECRET_KEY (cat .ds_secret_key)
```

### Database password

Same as with the secret key:

Either set the `DS_DB_PASSWORD` env variable directly, or read the key from a file.

For bash:

```bash
$ export DS_DB_PASSWORD=$(cat .ds_db_password)
```

For fish:

```fish
$ set -x DS_DB_PASSWORD (cat .ds_db_password)
```

### Setting the dev environment

Go to `dayliostats/settings.py` and set

```python
DEBUG = True
ADMIN = True
```

### Run the development server

For port 8000:

```
$ pipenv shell
$ ./manage.py runserver 8000
```

### Or use gunicorn

```
$ gunicorn dayliostats.wsgi
```

## Running tests

```
$ ./manage.py test
```

Pipenv should install `green` as a dependency for running tests. If not, try

```
$ pipenv install --dev
```
