from database import users_collection
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# -----------------------------------
# Create User
# -----------------------------------

def create_user(name, email, password):

    print("Received Name:", name)
    print("Received Email:", email)
    print("Received Password:", password)

    existing = users_collection.find_one({"email": email})

    if existing:
        return {
            "success": False,
            "message": "Email already exists."
        }

    hashed_password = pwd_context.hash(password)

    result = users_collection.insert_one({
        "name": name,
        "email": email,
        "password": hashed_password
    })

    print("User Saved!")

    return {
        "success": True,
        "message": "Account created successfully.",
        "user_id": str(result.inserted_id),
        "name": name,
        "email": email
    }


# -----------------------------------
# Login User
# -----------------------------------

def login_user(email, password):

    print("Login Attempt:", email)

    user = users_collection.find_one({
        "email": email
    })

    if user is None:
        return {
            "success": False,
            "message": "Invalid email."
        }

    if not pwd_context.verify(password, user["password"]):
        return {
            "success": False,
            "message": "Incorrect password."
        }

    return {
        "success": True,
        "message": "Login successful.",
        "user_id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"]
    }