from app.repository import appUserRepository
from flask import session

def fetchAll():
    return appUserRepository.fetchAll()

def fetchCategory(data):
    category = data.get("category")
    if not category:
        return appUserRepository.fetchAll()
    return appUserRepository.fetchCategory(category)

def add_to_cart(data):
    username = session['username']
    product_id = data.get('product_id')
    size = data.get('size')
    color = data.get('color')

    return appUserRepository.add_to_cart(username, product_id, color, size)

def remove_from_cart(data):
    product_id = data.get('product_id')
    size = data.get('size')
    color = data.get('color')
    username = session['username']

    response = appUserRepository.remove_from_cart(product_id, username, size, color)

    if response:
        return True
    return False

def get_cart():
    username = session['username']
    return appUserRepository.get_cart(username)

def finalize(data):
    phone = data.get("phone")
    city = data.get("city")
    address = data.get("address")
    building = data.get("building")
    floor = data.get("floor")
    email = data.get("email")

    if len(phone) != 8:
        return 'Invalid phone number', 400
    if len(city) < 3 :
        return 'Invalid City Name', 400
    if len(address) < 3:
        return 'Invalid Address', 400
    if int(floor) < 0:
        return 'Invalid Floor Number', 400
    if (not '@' in email) or (not '.' in email) or (email.count('.') > 2) or (email.count('@') > 1):
        return 'Invalid Email', 400
    
    username = session['username']
    
    return appUserRepository.finalize(username, phone, city, address, building, floor, email)

def get_images(product_id):
        return appUserRepository.get_images(product_id)