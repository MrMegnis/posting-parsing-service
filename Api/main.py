from dotenv import load_dotenv
from flask import Flask
from Api.orders_api import orders_api
from Api.users_api import users_api
from Api.errors import errors
from data import db_session

app = Flask(__name__)

app.register_blueprint(orders_api)
app.register_blueprint(users_api)
app.register_blueprint(errors)

if __name__ == "__main__":
    load_dotenv('.env')
    db_session.global_init()
    app.run(host="0.0.0.0", port=3000, debug=True)
