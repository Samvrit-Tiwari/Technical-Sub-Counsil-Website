import firebase_admin
from firebase_admin import credentials, firestore

# ==========================================
# 1. INITIALIZE FIREBASE ADMIN SDK
# ==========================================
KEY_PATH = "tsc-website-v1-0-0-firebase-adminsdk-fbsvc-6dc338e454.json"

try:
    cred = credentials.Certificate(KEY_PATH)
    firebase_admin.initialize_app(cred)
    print("✓ Firebase Admin SDK initialized successfully.")
except Exception as e:
    print(f"✕ Failed to initialize Firebase: {e}")
    exit(1)

db = firestore.client()

# ==========================================
# 2. SAMPLE DATASETS
# ==========================================

SECRETARIES = [
    {
        "name": "Krishan Murari Gupta - EE 27",
        "role": "General Secretary",
        "tenure": "2025 – Present",
        "current": True,
        "connect": "250137043@gmail.com",
        "photo": "./assets/secretaries/sana_iyer.jpg"
    },
    {
        "name": "Arnav Pandey - Chem 27",
        "role": "Joint Secretary (Tech)",
        "tenure": "2025 – Present",
        "current": True,
        "connect": "250137043@gmail.com",
        "photo": ""
    },
    {
        "name": "Aman Deep Verma",
        "role": "General Secretary",
        "tenure": "2024 – 2025",
        "current": False,
        "connect": "250137043@gmail.com",
        "photo": ""
    },
    {
        "name": "Riddhi Sharma",
        "role": "General Secretary",
        "tenure": "2023 – 2024",
        "current": False,
        "connect": "250137043@gmail.com",
        "photo": ""
    },
    {
        "name": "Vikramaditya Rao",
        "role": "General Secretary",
        "tenure": "2022 – 2023",
        "current": False,
        "connect": "250137043@gmail.com",
        "photo": ""
    }
]

ACHIEVEMENTS = [
    {
        "title": "Smart India Hackathon",
        "badge": "National Winner · 2025",
        "desc": "1st Place out of 1,200+ teams nationwide for creating an automated rural grid load management solution in the hardware edition.",
        "featured": True
    },
    {
        "title": "ICPC Regional Finals",
        "badge": "International Finalist · 2025",
        "desc": "Byte Battalion secured a top collegiate ranking at the regional competitive programming finals with sub-minute execution speeds.",
        "featured": True
    },
    {
        "title": "TechFest PCB Design Sprint",
        "badge": "1st Position · 2025",
        "desc": "Team CircuitBreakers won top honors for high-frequency multilayer impedance matching & micro-soldering under strict 24-hour limits.",
        "featured": True
    },
    {
        "title": "Kaggle Campus AI Challenge",
        "badge": "Top 10 Global · 2025",
        "desc": "Neural Nomads engineered lightweight quantized vision models, ranking top 10 on the real-time inference leaderboard.",
        "featured": True
    },
    {
        "title": "National Robowars Championship",
        "badge": "Runner-up · 2024",
        "desc": "Team Vortex built a 30kg combat-grade pneumatic flipper bot, securing 2nd place through four knockout matches.",
        "featured": False
    }
]

EVENTS = [
    {
        "name": "CircuitStorm — PCB Design Sprint",
        "date": "14 Nov 2025",
        "domain": "electronics",
        "tag": "Electronics",
        "desc": "48-hour PCB design and soldering challenge for first-year through final-year students.",
        "drive": "#"
    },
    {
        "name": "HackNorth 2025",
        "date": "02 Oct 2025",
        "domain": "coding",
        "tag": "Coding",
        "desc": "24-hour inter-college hackathon with 40 teams building for the campus life theme.",
        "drive": "#"
    },
    {
        "name": "RoboRumble Arena",
        "date": "19 Sep 2025",
        "domain": "robotics",
        "tag": "Robotics",
        "desc": "Combat and maze-solving robotics event with live elimination rounds.",
        "drive": "#"
    },
    {
        "name": "NeuralNight — ML Bootcamp",
        "date": "27 Aug 2025",
        "domain": "ai",
        "tag": "AI/ML",
        "desc": "Weekend bootcamp on model training, ending in a Kaggle-style leaderboard contest.",
        "drive": "#"
    },
    {
        "name": "SensorSprint IoT Jam",
        "date": "10 Aug 2025",
        "domain": "iot",
        "tag": "IoT",
        "desc": "Build-a-thon around low-power sensor networks and campus automation ideas.",
        "drive": "#"
    }
]

LEADS = [
    {"name": "Ananya Rao", "role": "Chairperson", "domain": "Robotics & Automation"},
    {"name": "Kabir Malhotra", "role": "Vice Chairperson", "domain": "Software Systems"},
    {"name": "Sana Iyer", "role": "General Secretary", "domain": "AI/ML"},
    {"name": "Devansh Oberoi", "role": "Treasurer", "domain": "Electronics"}
]

CORE = [
    {"name": "Ritika Sen", "role": "Events Lead", "domain": "Coding"},
    {"name": "Aarav Chauhan", "role": "Design Lead", "domain": "UI/UX"},
    {"name": "Meher Kaur", "role": "Logistics Lead", "domain": "Electronics"},
    {"name": "Yash Trivedi", "role": "Sponsorship Lead", "domain": "IoT"},
    {"name": "Ishita Bhatt", "role": "Media Lead", "domain": "Content"},
    {"name": "Rohan Deshpande", "role": "Technical Lead", "domain": "Robotics"}
]

TEAMS = [
    {
        "name": "Team Vortex",
        "tag": "Robotics",
        "achievements": ["1st — Smart India Hackathon 2025", "2nd — Robowars Nationals 2024"]
    },
    {
        "name": "Byte Battalion",
        "tag": "Competitive Programming",
        "achievements": ["Finalist — ICPC Regionals 2025", "1st — Inter-college CodeRelay 2025"]
    },
    {
        "name": "Neural Nomads",
        "tag": "AI/ML",
        "achievements": ["1st — HackNorth AI Track 2025", "Top 10 — Kaggle Campus Challenge"]
    },
    {
        "name": "CircuitBreakers",
        "tag": "Electronics",
        "achievements": ["1st — TechFest PCB Design 2025"]
    }
]

SHOP_ITEMS = [
    {
        "name": "Arduino Uno Starter Kit",
        "spec": "Board + breadboard + 40 jumper wires",
        "rate": "₹40/day",
        "stock": "in"
    },
    {
        "name": "DSLR Camera (Canon 200D)",
        "spec": "For event coverage & video projects",
        "rate": "₹250/day",
        "stock": "low"
    },
    {
        "name": "Soldering Station",
        "spec": "Temperature-controlled, 60W",
        "rate": "₹60/day",
        "stock": "in"
    },
    {
        "name": "Raspberry Pi 4 Kit",
        "spec": "4GB RAM, case, power supply, SD card",
        "rate": "₹120/day",
        "stock": "in"
    },
    {
        "name": "Digital Multimeter",
        "spec": "Auto-ranging, includes probes",
        "rate": "₹30/day",
        "stock": "in"
    },
    {
        "name": "Drone (FPV Racing)",
        "spec": "For aerial robotics & vision projects",
        "rate": "₹300/day",
        "stock": "low"
    }
]

# Stored using exact custom IDs (for instant ID-lookup during verification)
CERTIFICATES = {
    "TSC-2025-0417": {
        "name": "Priya Nambiar",
        "event": "HackNorth 2025",
        "date": "02 Oct 2025",
        "status": "Winner"
    },
    "TSC-2025-0982": {
        "name": "Arjun Mehta",
        "event": "RoboRumble Arena",
        "date": "19 Sep 2025",
        "status": "Participant"
    },
    "TSC-2024-1130": {
        "name": "Sneha Kulkarni",
        "event": "CircuitStorm 2024",
        "date": "11 Nov 2024",
        "status": "Runner-up"
    }
}

# ==========================================
# 3. BATCH SEEDING FUNCTION
# ==========================================
def seed_database():
    print("\nStarting batch seed to Firestore...")
    batch = db.batch()

    collections_map = {
        "secretaries": SECRETARIES,
        "achievements": ACHIEVEMENTS,
        "events": EVENTS,
        "leads": LEADS,
        "core": CORE,
        "teams": TEAMS,
        "shop": SHOP_ITEMS
    }

    # 1. Seed regular collections with auto-generated document IDs
    for col_name, items in collections_map.items():
        for item in items:
            doc_ref = db.collection(col_name).document()
            batch.set(doc_ref, {**item, "created_at": firestore.SERVER_TIMESTAMP})
        print(f"  → Staged {len(items)} items for collection: '{col_name}'")

    # 2. Seed certificates using their specific Certificate IDs as Document keys
    for cert_id, cert_data in CERTIFICATES.items():
        doc_ref = db.collection("certificates").document(cert_id)
        batch.set(doc_ref, {**cert_data, "created_at": firestore.SERVER_TIMESTAMP})
    print(f"  → Staged {len(CERTIFICATES)} items for collection: 'certificates'")

    # Commit all writes atomically
    batch.commit()
    print("\n✓ Database successfully seeded with all initial data!")

if __name__ == "__main__":
    seed_database()