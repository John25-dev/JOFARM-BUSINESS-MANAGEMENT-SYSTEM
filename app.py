import os
from workers import asgi
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from functools import wraps

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

# --- Security Gatekeeper (Tiered Rights Management) ---
def roles_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        async def decorated_function(env, *args, **kwargs):
            user_role = request.headers.get('X-User-Role') 
            if not user_role or user_role not in allowed_roles:
                return jsonify({"error": "Forbidden: Access level restricted"}), 403 [cite: 71]
            return await f(env, *args, **kwargs)
        return decorated_function
    return decorator

# --- NEW: Registration (Company Emails Only) ---
@app.route('/api/register', methods=['POST'])
async def register(env):
    data = request.get_json()
    email = data.get('email', '').lower()
    username = data.get('username')
    password = data.get('password')

    if not email.endswith("@jofarm.com"):
        return jsonify({"error": "Only @jofarm.com emails allowed"}), 403

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    role = "SUBORDINATE" # Default role for new signups

    try:
        await env.DB.prepare("INSERT INTO User (email, username, password_hash, role) VALUES (?, ?, ?, ?)") \
            .bind(email, username, hashed_pw, role).run()
        return jsonify({"status": "success"}), 201
    except:
        return jsonify({"error": "User already exists"}), 400

# --- Authentication ---
@app.route('/api/login', methods=['POST'])
async def login(env):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = await env.DB.prepare("SELECT * FROM User WHERE username = ? OR email = ?") \
        .bind(username, username).first() [cite: 72]

    if user and bcrypt.check_password_hash(user['password_hash'], password):
        return jsonify({"status": "success", "role": user['role'], "username": user['username']})
    
    return jsonify({"error": "Invalid credentials"}), 401

# --- Tiered Routes ---
@app.route('/api/admin/financials', methods=['GET'])
@roles_required('CEO', 'COUNTRY MANAGER') [cite: 73]
async def get_financials(env):
    return jsonify({"revenue": "UGX 14,500,000", "scope": "Global"})

# Worker Entrypoint
async def on_fetch(request, env):
    return await asgi.fetch(app, request, env)
