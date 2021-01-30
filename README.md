## Running server from docker ##
```
docker pull aliowka/sessionizer
docker run -p 5000:5000 aliowka/sessionizer
```
Navigate in browser to the link http://localhost:5000

## Running server from sourcecode ##
```
git clone http://github.com/aliowka/sessionizer`
cd sessionizer
```

### Create the environment ###
```
python3 -m venv venv
```

### Activate the environment ###
```
source venv/bin/activate
```

### Install project dependencies ###
```
pip install -r requirements.txt
```

### Run tests ###
```
export PYTHONPATH=$(pwd)
export FLASK_APP src/app.py
pytest tests -v
```

### Run web-server ###
```
flask run
```

The server will start on http://localhost:5000/ 
