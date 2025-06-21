from flask import current_app
import os
from werkzeug.utils import secure_filename
from app.repository import productRepository, authRepository

def add_product(data):
    price = data.form.get('price')
    category = data.form.get('category')
    sizes = data.form.get('sizes')
    colors = data.form.get('colors')
    images = data.files.getlist('images')

    #image_path = None
    #if image:
        #filename = secure_filename(image.filename)
        #image_path = f'images/{filename}'
        #image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

    res = productRepository.save(colors, category, price, sizes, images)

    if res:
        return True
    return False

def updateProduct(data):
    id = data.get('id')
    if not id:
        return False
    colors = data.get('colors')
    xsmall = data.get('xsmall')
    small = data.get('small')
    medium = data.get('medium')
    large = data.get('large')
    xlarge = data.get('xlarge')
    unit_price = data.get('unit_price')
    category = data.get('category')

    res = productRepository.update(id, colors, xsmall, small, medium, large, xlarge, unit_price, category)

    if res:
        return True
    return False

def deleteProduct(data):
    product_id = data.get('product_id')

    if not product_id:
        return False
    
    res = productRepository.delete(product_id)

    if res:
        return True
    return False

def view_orders():
    response = productRepository.view_orders()
    if not response:
        return False
    return response

def fetchadminuser():
    return authRepository.get_admin()

def fetchadminpass():
    return authRepository.get_admin_pass()

def fetchAll():
    return productRepository.fetchAll()

def fetchCategory(data):
    category = data.get("category")
    if not category:
        return productRepository.fetchAll()
    return productRepository.fetchCategory(category)