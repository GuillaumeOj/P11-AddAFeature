[![Mergify Status][mergify-status]][mergify]
![CI](https://github.com/GuillaumeOj/P11-AddAFeature/workflows/CI/badge.svg)
[![Code style: black][black-badge]][black]
[![Coverage Status][coverage-status]][coverage]

[mergify]: https://mergify.io
[mergify-status]: https://img.shields.io/endpoint.svg?url=https://gh.mergify.io/badges/GuillaumeOj/P11-AddAFeature&style=flat

[black]: https://github.com/psf/black
[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg

[coverage]: https://coveralls.io/github/GuillaumeOj/P11-AddAFeature?branch=master
[coverage-status]: https://coveralls.io/repos/github/GuillaumeOj/P11-AddAFeature/badge.svg?branch=master

# Contents page
- [I. What is PurBeurre?](#i-what-is-purbeurre)
- [II. Install](#ii-install-and-run)
- [III. Tests](#iii-test)
- [IV. To do list](#iv-to-do-list)
- [V. Technologies and ressources](#v-technologies-and-ressources)

# I. What is PurBeurre?
[⇧ *Top*](#contents-page)

The aim of this application is to propose a substitute for a food product.
The application use the open database provide by the [Open Food Facts](https://world.openfoodfacts.org/).
This application is made for the project 8 from [OpenClassrooms'](https://openclassrooms.com/fr/paths/68/projects/159/assignment) Python course
and reused for the projects 10 and 11.

The application is alive here => https://projet-11.ojardias.io

# II. Install and run
[⇧ *Top*](#contents-page)

To install this project on your computer you'll need **Postgresql**, **Python 3.9** ans **Tox**.

First clone this repository:
```bash
git@github.com:GuillaumeOj/Pur-Beurre.git
or
https://github.com/GuillaumeOj/Pur-Beurre.git
```

## Configure

In the project directory:
```bash
cp env-example .env-local
```

Edit `.env-local` and replace parameters by yours:
```bash
POSTGRES_DB='your-database-name'
POSTGRES_USER='user-allowed-to-access-the-database'
POSTGRES_HOST='localhost' # Default parameter
POSTGRES_PORT=5432        # Default parameter
```

## Init the database
```bash
tox -e init-db
```

## Run the application
```bash
tox -e start
```

## Update the application

First update the file for the repository:
```bash
git pull
```

Then use:
```bash
tox -e update-app
```

You're ready to run the application!

# III. Tests 
[⇧ *Top*](#contents-page)

Tests with `pytest`:
```bash
tox -e py39
```

Test for `pep8`:
```bash
tox -e pep8
```

Coverage with `coverage.py`:
```bash
tox -e coverage
```

# IV. To do list
[⇧ *Top*](#contents-page)

See my [Notion's board](https://www.notion.so/guillaumeoj/c79895c9cf514fe0ae1ff4d535d42308?v=0d9c86e1912149bcbbc329277ca46819)

# V. Technologies and ressources
[⇧ *Top*](#contents-page)

This application use various technologies and ressources.

- Main language  => [Python 3.9](https://www.python.org/)
- Framework => [Django](https://www.djangoproject.com/)
- Database => [Postgresql](https://www.postgresql.org/)
- Front => [Bootstrap](https://getbootstrap.com/)
- Template => [Creative from Start Bootstrap](https://startbootstrap.com/themes/creative/)
- Merging PR => [Mergify.io](https://mergify.io/)
- Tests => [Pytest](http://docs.pytest.org/en/latest/)
- Pep8 => [Flake8](http://flake8.pycqa.org/)
- Code style => [Black](https://github.com/psf/black)
- Import sorting => [Isort](https://pycqa.github.io/isort/)
- Coverage => [Coverage.py](https://github.com/nedbat/coveragepy) and [Coveralls](https://coveralls.io/)
- Continuous Integration => [Github Actions](https://github.com/features/actions)
- Hosting => [DigitalOcean](https://www.digitalocean.com/)
