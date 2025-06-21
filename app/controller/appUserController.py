from flask import Blueprint, render_template, redirect, url_for, session, request
from app.service import appUserService

user_bp = Blueprint('user', __name__)

@user_bp.route("/profile")
def profile():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    return "User Profile"

@user_bp.route("/contact-us")
def contact():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    return render_template('contact.html')

@user_bp.route("/products-page")
def products_page():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    products = appUserService.fetchAll()
    categories = sorted(set(p['category'] for p in products))
    return render_template("product.html", products=products, categories=categories)

@user_bp.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    data = request.form
    response =  appUserService.add_to_cart(data)

    if not response:
        return 'Item not found', 400
    return 'Ok', 200

@user_bp.route("/remove-from-cart", methods=["DELETE"])
def remove_from_cart():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    data = request.get_json()
    response =  appUserService.remove_from_cart(data)

    if not response:
        return 'Failed to remove product from cart', 400
    return 'Ok', 200

@user_bp.route("/cart", methods=['GET'])
def cart():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    cart_items = appUserService.get_cart()
    total = sum(item['unit_price'] for item in cart_items)

    return render_template("cart.html", cart=cart_items, total=total)

@user_bp.route("/checkout", methods=['GET'])
def checkout():
    if 'username' not in session:
        return "Unauthorized", 401
    return render_template("checkout.html")

@user_bp.route("/finalize", methods=['POST'])
def finalize():
    if 'username' not in session:
        return "Unauthorized", 401

    data = request.get_json()
    response = appUserService.finalize(data)

    if type(response) == bool:
        if not response:
            return 'Error placing Order', 400
        return 'Ok', 200
    
    if isinstance(response, tuple) and response[1] == 400:
        return {"error": response[0]}, 400
    
@user_bp.route("/filter-by-category", methods=['POST'])
def fetchCategory():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    data = request.get_json()
    products = appUserService.fetchCategory(data)
    return products, 200

@user_bp.route("/product-images/<int:product_id>")
def product_images(product_id):
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    response = appUserService.get_images(product_id)
    images = [row[0] for row in response]

    return render_template("product_images.html", images=images)
