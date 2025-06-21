from app.repository import authRepository

def find_admin(data):
    username = data.get("username")
    password = data.get("password")
    admin = authRepository.find_admin(username, password)
    if not admin:
        return False
    return True

def find(data):
    username = data.get("username")
    password = data.get("password")
    user = authRepository.find(username, password)
    if not user:
        return False
    return True 

def addUser(data):
    username = data.get("username")
    password = data.get("password")
    if authRepository.findIfUsernameTaken(username):
        return False  # Username taken
    return authRepository.add(username, password) # True if added, False otherwise