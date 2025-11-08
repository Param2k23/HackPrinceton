import bcrypt
import json

def generate_password_hash(password: str) -> str:
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# Read the current database
with open('user_database.json', 'r') as f:
    db = json.load(f)

# Set simple passwords for testing
passwords = {
    "john_doe": "parent123",
    "sam": "parent456",
    "emily": "child123"
}

# Update password hashes
for username, password in passwords.items():
    if username in db["current_users"]:
        db["current_users"][username]["password"] = generate_password_hash(password)

# Write back to the database
with open('user_database.json', 'w') as f:
    json.dump(db, f, indent=4)

print("Updated passwords:")
for username, password in passwords.items():
    print(f"{username}: {password}")