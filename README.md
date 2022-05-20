# [UBCGrades](https://ubcgrades.com/)

This is the source code for https://ubcgrades.com/. This repo is a [Flask](https://flask.palletsprojects.com/en/1.1.x/) website with the front end using jQuery and Bootstrap. 

## Project Structure

```
< PROJECT ROOT >
   |
   |-- app/                      # Implements app logic
   |    |-- api/				 # API Blueprint - RESTful interface for devices and other management
   |    |-- main/                # Main Blueprint - Serves pages
   |    |-- static/              # Static content (JS, CSS, images)
   |    |-- templates/           # Jinja2 templates
   |    |-- tests/               # Tests
   |    |
   |    __init__.py              # Initialize the app
   |
   |-- ubc-pair-grade-data/      # Data submodule dependency
   |
   |-- requirements.txt          # Development modules
   |-- config.py                 # Set up the app
   |-- run.py                    # Start the app - WSGI gateway
```

## Development

```bash
$ # Clone the sources
$ git clone https://github.com/DonneyF/ubcgrades.git
$ cd ubcgrades
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv --no-site-packages env
$ source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv --no-site-packages env
$ # .\env\Scripts\activate
$ 
$ # Install requirements
$ pip3 install -r requirements.txt
$
$ # Set the FLASK_APP environment variable
$ (Unix/Mac) export FLASK_APP=run.py
$ (Windows) set FLASK_APP=run.py
$ (Powershell) $env:FLASK_APP = ".\run.py"
$
$ # Set up the DEBUG environment
$ # (Unix/Mac) export FLASK_ENV=development
$ # (Windows) set FLASK_ENV=development
$ # (Powershell) $env:FLASK_ENV = "development"
$
$ # Run the application
$ # --host=0.0.0.0 - expose the app on all network interfaces (default 127.0.0.1)
$ # --port=5000    - specify the app port (default 5000)  
$ flask run --host=0.0.0.0 --port=5000
$
$ # Access the app in browser: http://127.0.0.1:5000/
```

## Credits

The template of this repo was built off the [Flask Argon Dashboard](https://github.com/app-generator/flask-argon-dashboard).

