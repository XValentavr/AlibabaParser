from flask import Flask
from flask_cors import CORS

from routers.get_amazon_url import amazon_link

application = Flask(__name__)
application.register_blueprint(amazon_link)
CORS(application)

if __name__ == "__main__":
    application.run(port=5001, host="0.0.0.0")
