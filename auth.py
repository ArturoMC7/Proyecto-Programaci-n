import json

def load_users():
    try:
        with open('users.json', 'r') as f: return json.load(f)
    except FileNotFoundError: return {"users": []}

def save_users(data):
    with open('users.json', 'w') as f: json.dump(data, f, indent=4)

def findUser(user):
    data = load_users()
    for u in data['users']:
        if u['user'] == user: return u
    return None

def registerUser(user, password, role, email="", age=""):
    data = load_users()
    for u in data['users']:
        if u['user'] == user: return "user already exists"
    
    new_user = {
        "user": user, "password": password, "role": role, 
        "email": email, "age": age, "session": False
    }
    data['users'].append(new_user)
    save_users(data)
    return "ok"

def openCloseSession(user, password, flag):
    data = load_users()
    for u in data['users']:
        if u['user'] == user:
            if u['password'] == password:
                u['session'] = flag
                save_users(data)
                return u # Devolvemos todo el objeto del usuario para el Frontend
            else: return "wrong credentials"
    return "wrong credentials"

def hasRole(user, roles):
    data = load_users()
    for u in data['users']:
        if u['user'] == user: return u.get('role') in roles
    return False