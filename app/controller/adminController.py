from flask import Flask, request, Blueprint, render_template, session
from app.service import adminService

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/admin-page", methods=['GET'])
def admin_page():
    if ('username' not in session) or (session['username'] != adminService.fetchadminuser()) or (session['password'] != adminService.fetchadminpass()) or (session['role'] != 'admin'):
        return '', 404
    return render_template("admin_page.html")

@admin_bp.route("/add-product", methods=['GET', 'POST'])
def add_product():
    if ('username' not in session) or (session['username'] != adminService.fetchadminuser()) or (session['password'] != adminService.fetchadminpass()) or(session['role'] != 'admin'):
        return '', 404
    if request.method == 'GET':
        return render_template("admin_controls.html")
    else:
        response = adminService.add_product(request)
        if (response):
            return 'Ok', 200
        return 'Error cannot add item', 400

@admin_bp.route("/update-product", methods=['PUT'])
def update_product():
    if ('username' not in session) or (session['username'] != adminService.fetchadminuser()) or (session['password'] != adminService.fetchadminpass()) or(session['role'] != 'admin'):
        return '', 404
    data = request.get_json()
    response = adminService.updateProduct(data)
    if (response):
        return 'Ok', 200
    return 'Error cannot update item', 400

@admin_bp.route("/delete-product", methods=['DELETE'])
def delete_product():
    if ('username' not in session) or (session['username'] != adminService.fetchadminuser()) or (session['password'] != adminService.fetchadminpass()) or(session['role'] != 'admin'):
        return '', 404
    data = request.get_json()
    print(data)
    response = adminService.deleteProduct(data)
    if (response):
        return 'Ok', 200
    return 'Error cannot delete item', 400

@admin_bp.route("/view-orders", methods=['GET'])
def view_orders():
    if ('username' not in session) or (session['username'] != adminService.fetchadminuser()) or (session['password'] != adminService.fetchadminpass()) or(session['role'] != 'admin'):
        return '', 404
    orders = adminService.view_orders()
    if not orders:
        orders = []
    return render_template("view_orders.html", orders=orders)

@admin_bp.route("/view-products", methods=['GET'])
def products_page():
    if ('username' not in session) or (session['username'] != adminService.fetchadminuser()) or (session['password'] != adminService.fetchadminpass()) or(session['role'] != 'admin'):
        return '', 404
    products = adminService.fetchAll()
    categories = sorted(set(p['category'] for p in products))
    return render_template("admin_products_page.html", products=products, categories=categories)

@admin_bp.route("/admin-filter-product", methods=['POST'])
def admin_filter_product():
    if ('username' not in session) or (session['username'] != adminService.fetchadminuser()) or (session['password'] != adminService.fetchadminpass()) or(session['role'] != 'admin'):
        return '', 404
    data = request.get_json()
    products = adminService.fetchCategory(data)
    return products, 200