from sqlalchemy import text
from flask import jsonify
from app.db import db
import cloudinary.uploader


def save(colors, category, price, sizes, images):
    insert_sql = text("""
    INSERT INTO product (unit_price, category)
    VALUES (:unit_price, :category)
    RETURNING product_id
    """)
    result = db.session.execute(insert_sql, {
        "unit_price": price,
        "category": category.title()
    })
    product_id = result.scalar()

    sizes = sizes.split(',')
    for size in sizes:
        if size=="":
            continue
        size = size.strip().upper()
        db.session.execute(
            text("INSERT INTO product_size (product_id, size) VALUES (:id, :size)"),
            {"id": product_id, "size": size}
        )

    colors = colors.split(',')
    for color in colors:
        if color=="":
            continue
        color = color.strip().title()
        db.session.execute(
            text("INSERT INTO product_color (product_id, color) VALUES (:id, :color)"),
            {"id": product_id, "color": color}
        )


    for image in images:
        if image:
            result = cloudinary.uploader.upload(image)
            image_url = result['secure_url']

            db.session.execute(
                text("INSERT INTO product_image (product_id, image_path) VALUES (:id, :image_path)"),
                {"id": product_id, "image_path": image_url}
            )

            print("Uploaded:", image_url)

    try:
        db.session.commit()
    except Exception:
        return False

    return True


def delete(product_id):
    db.session.execute(text("DELETE FROM product_color WHERE product_id = :id"), {'id': product_id})
    db.session.execute(text("DELETE FROM product_size WHERE product_id = :id"), {'id': product_id})
    db.session.execute(text("DELETE FROM product_image WHERE product_id = :id"), {'id': product_id})
    db.session.execute(text("DELETE FROM product WHERE product_id = :id"), {'id': product_id})

    try:
        db.session.commit()
    except Exception:
        return False

    return True

def view_orders():
    orders_data = db.session.execute(text("SELECT * FROM orders")).fetchall()
    orders = []
    
    for order_row in orders_data:
        order = dict(order_row._mapping)
        total_price = 0.0

        ordered_products_data = db.session.execute(text("""
            SELECT 
                p.product_id,
                p.unit_price,
                p.category,
                op.size,
                op.color
            FROM ordered_product op
            JOIN product p ON p.product_id = op.product_id
            WHERE op.order_id = :order_id
        """), {"order_id": order["order_id"]}).fetchall()
        

        order["items"] = []

        for item in ordered_products_data:
            item = dict(item._mapping)
            total_price+=float(item['unit_price'])

            product_id = item['product_id']
            image = db.session.execute(text("SELECT pm.image_path FROM product_image pm WHERE pm.product_id = :product_id"), {
            "product_id": product_id
            }).fetchall()
            item['image_path'] = image[0][0]

            order["items"].append(item)
        order['total_price'] = total_price

        orders.append(order)

    return orders

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