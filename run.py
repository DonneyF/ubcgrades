from app import create_app
from config import Config

app, db = create_app(Config)
app.run()
