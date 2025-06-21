from flask import jsonify
from sqlalchemy import text
from app.db import db

def fetchAll():
    query = """
        SELECT 
            p.product_id,
            p.unit_price,
            p.category,
            json_agg(DISTINCT ps.size) AS sizes,
            json_agg(DISTINCT pc.color) AS colors,
            json_agg(DISTINCT pm.image_path) AS image_path
        FROM product p
        LEFT JOIN product_size ps ON p.product_id = ps.product_id
        LEFT JOIN product_color pc ON p.product_id = pc.product_id
        LEFT JOIN product_image pm ON p.product_id = pm.product_id
        GROUP BY p.product_id, p.unit_price, p.category
    """

    data = db.session.execute(text(query))
    products = [dict(row._mapping) for row in data]
    return products


def fetchCategory(category):
    data = db.session.execute(text("""SELECT 
            p.product_id,
            p.unit_price,
            p.category,
            json_agg(DISTINCT ps.size) AS sizes,
            json_agg(DISTINCT pc.color) AS colors,
            json_agg(DISTINCT pm.image_path) AS image_path
        FROM product p
        LEFT JOIN product_size ps ON p.product_id = ps.product_id
        LEFT JOIN product_color pc ON p.product_id = pc.product_id
        LEFT JOIN product_image pm ON p.product_id = pm.product_id
        WHERE p.category = :category
        GROUP BY p.product_id, p.unit_price, p.category
        """), {
        "category" : category
    })
    products = [dict(row._mapping) for row in data]
    return jsonify(products)

def add_to_cart(username, product_id, color, size):
    item = db.session.execute(text("""
        SELECT p.unit_price, p.category, pc.color, ps.size
        FROM product p
        JOIN product_color pc ON p.product_id = pc.product_id
        JOIN product_size ps ON p.product_id = ps.product_id
        WHERE p.product_id = :product_id
        AND pc.color = :color
        AND ps.size = :size
    """), {
        "product_id": product_id,
        "color": color,
        "size": size
    }).fetchone()

    if not item:
        return False  

    db.session.execute(text("""
        INSERT INTO cart (product_id, color, size, username)
        VALUES (:product_id, :color, :size, :username)
    """), {
        "product_id": product_id,
        "username": username,
        "color": color,
        "size": size
    })
    db.session.commit()

    return True

def remove_from_cart(product_id, username, size, color):
    db.session.execute(text("""
        DELETE FROM cart WHERE username = :username AND product_id = :product_id AND size = :size AND color = :color
    """), {"username": username, "product_id": product_id, "size": size, "color": color})

    db.session.commit()
    return True

def get_cart(username):
    cart_items = db.session.execute(text("SELECT * FROM cart WHERE username = :username"), {
        "username": username
    }).fetchall()

    product_dicts = []
    for item in cart_items:
        size = item._mapping['size']
        color = item._mapping['color']
        product_id = item._mapping['product_id']
        product = db.session.execute(text("SELECT p.unit_price, p.category FROM product p WHERE p.product_id = :product_id"), {
            "product_id": product_id
        }).fetchone()

        image = db.session.execute(text("SELECT pm.image_path FROM product_image pm WHERE pm.product_id = :product_id"), {
            "product_id": product_id
        }).fetchall()


        if product:
            product_data = dict(product._mapping)
            product_data['size'] = size
            product_data['color'] = color
            product_data['product_id'] = item._mapping['product_id']
            product_data['image_path'] = image[0][0]
            product_dicts.append(product_data)

    return product_dicts

def finalize(username, phone, city, address, building, floor, email):
    cart_items = db.session.execute(text("SELECT * FROM cart WHERE username = :username"), {
        "username": username
    }).fetchall()

    product_dicts = []
    for item in cart_items:
        size = item._mapping['size']
        color = item._mapping['color']
        product = db.session.execute(text("SELECT * FROM product p WHERE p.product_id = :product_id"), {
            "product_id": item._mapping['product_id']
        }).fetchone()

        if product:
            product_data = dict(product._mapping)
            product_data['size'] = size
            product_data['color'] = color
            product_dicts.append(product_data)

    db.session.execute(text("INSERT INTO orders (username, phone, city, address, building, floor, email) VALUES (:username, :phone, :city, :address, :building, :floor, :email)"), {
        "username": username,
        "phone": phone,
        "city" : city,
        "address" : address,
        "building" : building,
        "floor" : floor,
        "email" : email
        })
    
    order_id_result = db.session.execute(text("""
        SELECT MAX(order_id) AS order_id FROM orders WHERE username = :username
    """), {"username": username}).fetchone()

    order_id = order_id_result.order_id if order_id_result else None
    if not order_id:
        return False

    for product in product_dicts: #orderid and productid 
        db.session.execute(text("INSERT INTO ordered_product (order_id, product_id, color, size) VALUES (:order_id, :product_id, :color, :size)"), {
            "order_id": order_id,
            "product_id" : product['product_id'],
            "color": product['color'],
            "size": product['size']
        })

    db.session.execute(text("""
        DELETE FROM cart WHERE username = :username
    """), {"username": username})

    db.session.commit()
    return True

def get_images(product_id):
    query = """
        SELECT image_path FROM product_image WHERE product_id = :pid
    """
    result = db.session.execute(text(query), {"pid": product_id})

    return result
