from flask import Flask, session
from dotenv import load_dotenv
from app.db import db
import os
import cloudinary
from cloudinary.utils import cloudinary_url
from app.domain.models import app_user, admin, product, ordered_product, product_color, orders, cart, product_image, product_size

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_PERMANENT'] = False
    app.secret_key = os.getenv("SECRET_KEY")

    cloudinary.config(
        cloud_name=os.getenv("CLOUD_NAME"),
        api_key=os.getenv("CLOUD_API_KEY"),
        api_secret=os.getenv("CLOUD_API_SECRET"),
        secure=True
    )

    db.init_app(app)

    with app.app_context():
        db.create_all()
        
    from app.controller import register_controller
    register_controller(app)

    return app
