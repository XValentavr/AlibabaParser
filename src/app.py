from flask import Flask
from flask_cors import CORS

from clients.celery.celery_init_client import celery_client
from routers.get_amazon_url_route import amazon_link

application = Flask(__name__)
application.register_blueprint(amazon_link)

celery_app = celery_client.celery_init_app(application)

CORS(application)

if __name__ == "__main__":
    application.run(port=5001, host="0.0.0.0", debug=True)
