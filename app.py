import os
import json
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

app = Flask(__name__)
# Enable CORS for frontend integration
CORS(app)


creds = {
  "type": "service_account",
  "project_id": "tsc-website-v1-0-0",
  "private_key_id": "4d9bb0035820084cefd18c2f7913bb8d9b161a4e",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDLwDcGnBL1n9eA\nAcCTg7pZkbk5wlfJt7jk0l6bBbrI+ULJMcXMiTuON3g4Ey3/kBSlXbR83J7KHHRe\nx9YymS8FzSwxewunCc6esGVjRxYiPSElx0qKdByX8vD2hl10VB4647Y12CWSdflV\n7Wfem22Ec9ghIUVT83wuDsMX1YR50iiHs9nFlUSIC3DAL0H7YH/TB5zr7pVvyEA/\n7ETVW4quLe9oL4zVfzfXxgbUXN/pBaZ2hStjfGTOs8rbpvJtSXDHnZVY6DcXM64/\nRvasvjtCXSsI7VA2XfZnySuzshs44UTLm9DkUXS6f0mxLGXC2jFsCEP5pz2T7/ed\ndRfN7LVtAgMBAAECggEAJFi+uCwhabXA8LHfU7FdDdtkCnyzwmVG03L/s3HbNzzY\nACIj4e/dMuqMRJyPSRa/yBwmNVv5654V2E6X1GDlNYi7SHxlwL+MH1ziSUqGFUeI\nYT/i+T3rV+Pbvm6Lv1O+LM0wVPyg/zaSaxS1wc1CRS2RMZ/IyUgXL/QsM1VAk6Zr\nLqhP+hjjCTbZIPe23mZcaygpGhmN7j8yuyECq697t/FZabcBhD6uFuv8ZXSdwXOY\ngmUWvmZ90IYb0+Besquqy2VDbOV778+bcQkAxS3V5MLAjbNrbfZvZt0ZNV++zQNh\neqdUKB+J2oZ8S2fe68rYUVSX2ih2A805j/EAfbl0dQKBgQD0aZxVW0bELo/sqRNC\nec/fJQ6xJK0KD++CLH1F+vtH7pwjdwLqnA+ZD7UItV6lzF1RyUF5YwuMHQtCeZH3\nXAwb3XQifpViDLIQRy39KZxwM0uSDIfeUuR9e1WiN3koiGwli88CSaP/TnSAPJr7\n7DU3iPjSE5dszTkcwKlutyawMwKBgQDVaRnNdI65D6A1SU0YW18I1Ul5n2OHN+Gn\ntjN2Ijeh8q0Sn/LR7s5crsBnb9ZTYTtZbb/fCJTXOf3skCY5H4IwK3rdxfYOtjZO\nnx6bQ0Q8YrlHhLqObyNBUfSpxfOHtHXxgVeu4x7BVpNR4I+yw3IbRrz/fcfQVSDZ\n6tG9CxTj3wKBgQDeHF+ivhk4TWwj0J6dCZ/blIyedMr/2u14ab/KacQTYYbpP80Z\nsYsHONv2twP1PhwMKA3lJxomUXqbBWmd1jt20zAn7MsKWKk028qyRy9QU304k0Sh\nyMi2M+/lQ+5J5HgLQttzo8JyUDTVGL5rdAQEnOgp2P4CNRnSxE71O2HgOwKBgDEl\n3EhhwIDEJXxAHl4upMtO+3XkDDLW3sQWBPH+3VsRnWQ9q9lHKwVTRYJM0koviVCG\nIvsFaenLNDxn0jWzmPLpAInUjl9C/WzL3muZaTyS6+KZobEtzSu86SC0Muqc19C/\nnebr7WhPPOxNUCq2MjAv8VTRrdO/1yn4l0b3J193AoGAZgdjaUyHobPAVGSUq/CW\ngef+UUpW5MahBT0RjlF8jG+0jCPlwK2NZcyhbenkefSwUXs5/Ragnewq5MwzhxSQ\nA2BReGCRHnkv3r5s+z1O28tBcRZj60VXRpKMz1Z8MqoraFCvDIWUYMHs7CIZRzyo\nVST5H7ulcp4bW7oJDMYnxew=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@tsc-website-v1-0-0.iam.gserviceaccount.com",
  "client_id": "105285595672088599207",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40tsc-website-v1-0-0.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# ==========================================
# FIREBASE INITIALIZATION
# ==========================================

cred = credentials.Certificate(creds)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Allowed collections matching your frontend models
VALID_COLLECTIONS = {
    'events',
    'achievements',
    'leads',
    'core',
    'teams',
    'shop',
    'rentals',
    'secretaries',
    'certificates'
}

# ==========================================
# BULK SYNC ENDPOINTS
# ==========================================

@app.route('/api/bootstrap', methods=['GET'])
def get_all_site_data():
    """Fetches all collections in one go for fast client-side initialization."""
    response_data = {}
    try:
        for col_name in VALID_COLLECTIONS:
            docs = db.collection(col_name).stream()
            response_data[col_name] = [
                {**doc.to_dict(), "id": doc.id} for doc in docs
            ]
        return jsonify({"success": True, "data": response_data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==========================================
# GENERIC CRUD ENDPOINTS
# ==========================================

@app.route('/')
def home():
    return "hello_world"

@app.route('/api/<collection_name>', methods=['GET'])
def get_collection(collection_name):
    """Retrieve all documents from a specific collection."""
    if collection_name not in VALID_COLLECTIONS:
        return jsonify({"success": False, "error": f"Invalid collection: {collection_name}"}), 400

    try:
        docs = db.collection(collection_name).stream()
        data = [{**doc.to_dict(), "id": doc.id} for doc in docs]
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/<collection_name>', methods=['POST'])
def add_document(collection_name):
    """Create a new document in the given collection."""
    if collection_name not in VALID_COLLECTIONS:
        return jsonify({"success": False, "error": f"Invalid collection: {collection_name}"}), 400

    payload = request.get_json()
    if not payload:
        return jsonify({"success": False, "error": "No JSON payload provided"}), 400

    try:
        # If client sends a custom ID (e.g. for certificates), use it; otherwise auto-generate
        custom_id = payload.pop('id', None)
        payload['created_at'] = firestore.SERVER_TIMESTAMP

        if custom_id:
            doc_ref = db.collection(collection_name).document(custom_id)
            doc_ref.set(payload)
            doc_id = custom_id
        else:
            _, doc_ref = db.collection(collection_name).add(payload)
            doc_id = doc_ref.id

        return jsonify({"success": True, "id": doc_id, "message": "Document added"}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/<collection_name>/<doc_id>', methods=['PUT'])
def update_document(collection_name, doc_id):
    """Update fields on an existing document."""
    if collection_name not in VALID_COLLECTIONS:
        return jsonify({"success": False, "error": f"Invalid collection: {collection_name}"}), 400

    payload = request.get_json()
    if not payload:
        return jsonify({"success": False, "error": "No JSON payload provided"}), 400

    try:
        doc_ref = db.collection(collection_name).document(doc_id)
        payload.pop('id', None)  # Prevent writing ID to the inner document
        payload['updated_at'] = firestore.SERVER_TIMESTAMP
        doc_ref.update(payload)
        return jsonify({"success": True, "id": doc_id, "message": "Document updated"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/<collection_name>/<doc_id>', methods=['DELETE'])
def delete_document(collection_name, doc_id):
    """Delete a document by ID."""
    if collection_name not in VALID_COLLECTIONS:
        return jsonify({"success": False, "error": f"Invalid collection: {collection_name}"}), 400

    try:
        db.collection(collection_name).document(doc_id).delete()
        return jsonify({"success": True, "id": doc_id, "message": "Document deleted"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==========================================
# SPECIFIC ACTION ENDPOINTS
# ==========================================

@app.route('/api/verify-certificate/<cert_id>', methods=['GET'])
def verify_certificate(cert_id):
    """Quick lookup for single certificate verification."""
    try:
        doc_ref = db.collection('certificates').document(cert_id.upper())
        doc = doc_ref.get()
        if doc.exists:
            return jsonify({"success": True, "found": True, "data": doc.to_dict()}), 200
        else:
            return jsonify({"success": True, "found": False, "message": "Certificate not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/seed-defaults', methods=['POST'])
def seed_initial_data():
    """Optional helper endpoint to upload your starter data into Firestore in one call."""
    payload = request.get_json() or {}
    batch = db.batch()
    
    try:
        for col_name, items in payload.items():
            if col_name in VALID_COLLECTIONS:
                for item in items:
                    item_id = item.pop('id', None)
                    doc_ref = db.collection(col_name).document(item_id) if item_id else db.collection(col_name).document()
                    batch.set(doc_ref, item)
        batch.commit()
        return jsonify({"success": True, "message": "Database seeded successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0")