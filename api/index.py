import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
# Enable CORS for frontend integration
CORS(app)



if not firebase_admin._apps:
    firebase_creds_raw = os.environ.get("FIREBASE_CREDENTIALS_JSON")
    if not firebase_creds_raw:
        raise RuntimeError(
            "FIREBASE_CREDENTIALS_JSON environment variable is not set. "
            "Add it in your Vercel project's Environment Variables settings."
        )
    creds_dict = json.loads(firebase_creds_raw)
    cred = credentials.Certificate(creds_dict)
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


# Vercel's Python runtime calls the WSGI `app` object directly — no app.run() needed.
# Kept here only for local testing: `python api/index.py`
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
