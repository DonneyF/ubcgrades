from app import create_app
from config import Config

app, db = create_app(Config)

if __name__ == '__main__':
    app.run()
