## Running server from sourcecode ##
`git clone http://github.com/aliowka/sw-assignment`
`cd sw-assignment`

### Create the environmen ###
`python3 -m venv venv`

### Activate the environment ###
`source venv/bin/activate`

### Install project dependencies ###
`pip install -r requirements.txt`

### Run tests ###
`export PYTHONPATH=$(pwd)`
`pytest tests`

### Run web-server ###
`python web-server.py`

Ther server will start on http://localhost:5000/ 

## Running server from docker ##
`docker pull aliowka/sw-assigment`
`docker run -p 5000:5000`

## Executing queries ##
curl http://localhost:5000/

