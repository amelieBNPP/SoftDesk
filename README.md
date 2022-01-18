# openclassroom - projet10 - application Django RESTfull

| SoftDesk |
|:----------:|

_Owner: [Amélie](https://github.com/ameliebnpp)_

## Developpement guide

### General informations

This project is developped with DRF (DjangoRestFull) and follow the OWASP rules.

### Installation

1. Clone the project:

```bash
git clone --recursive git@github.com:amelieBNPP/SoftDesk.git
```
*Clone only one time the project.*

2. Create the virtual environement and activate it:
```bash
python -m venv .venv
source .venv/bin/activate
```
*The virtual environement is created only one time, however, it is activate each time we start to develop.*

### Dependencies

Install dependencies :

```bash
pip install -r requirements.txt
```
*Install dependancies each time we develop on this project.*

### Run server

Server can be run using the following commands:
```bash
python manage.py runserver
```

The API can be tested in local at the following adresse : http://localhost:8000/api/

### Tests

To ensure new features do not add any regression in the code, run the tests with the following commands : 
```bash
python manage.py test
```
### Postman documentation

List and description of all termination points are documented here: [postman documentation](https://documenter.getpostman.com/view/14836417/UVXkoFcn)

