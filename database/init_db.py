"""
JanSetu Database Initialization and Scheme Seeder
Initializes SQLite database with schema.sql and seeds demo schemes and citizen personas.
"""

import json
import os
import sqlite3
import sys
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "jansetu.db"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"
SEED_PATH = BASE_DIR / "database" / "schemes_seed.json"


def init_database():
    print(f"[*] Initializing database at: {DB_PATH}")
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Read and execute schema
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    cursor.executescript(schema_sql)
    conn.commit()
    print("[OK] Database schema applied successfully.")

    # Seed Schemes from schemes.json (or fallback to schemes_seed.json)
    schemes_json_path = BASE_DIR / "database" / "schemes.json"
    target_seed = schemes_json_path if schemes_json_path.exists() else SEED_PATH
    with open(target_seed, "r", encoding="utf-8") as f:
        schemes_data = json.load(f)

    for item in schemes_data:
        cursor.execute(
            """
            INSERT INTO schemes (
                code, name, name_hindi, ministry, category, target_audience,
                short_description, full_description, benefits, max_benefit_amount,
                eligibility_criteria_json, required_documents_json,
                application_process, official_url, level, state,
                verification_date, source, tags
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(code) DO UPDATE SET
                name=excluded.name,
                name_hindi=excluded.name_hindi,
                ministry=excluded.ministry,
                category=excluded.category,
                target_audience=excluded.target_audience,
                short_description=excluded.short_description,
                full_description=excluded.full_description,
                benefits=excluded.benefits,
                max_benefit_amount=excluded.max_benefit_amount,
                eligibility_criteria_json=excluded.eligibility_criteria_json,
                required_documents_json=excluded.required_documents_json,
                application_process=excluded.application_process,
                official_url=excluded.official_url,
                level=excluded.level,
                state=excluded.state,
                verification_date=excluded.verification_date,
                source=excluded.source,
                tags=excluded.tags
        """,
            (
                item["code"],
                item["name"],
                item.get("name_hindi", ""),
                item["ministry"],
                item["category"],
                item.get("target_audience", ""),
                item["short_description"],
                item.get("full_description", item["short_description"]),
                item["benefits"],
                item.get("max_benefit_amount", 0),
                json.dumps(item["eligibility_criteria"], ensure_ascii=False),
                json.dumps(item["required_documents"], ensure_ascii=False),
                item.get("application_process", ""),
                item.get("official_url", ""),
                item.get("level", "Central"),
                item.get("state", "All India"),
                item.get("verification_date", "unknown"),
                item.get("source", "myScheme Portal (myscheme.gov.in)"),
                item.get("tags", ""),
            ),
        )

    conn.commit()
    print(f"[OK] Successfully seeded {len(schemes_data)} welfare schemes from {target_seed.name}.")

    # Seed Demo Citizen Personas
    seed_demo_personas(cursor, conn)

    conn.close()
    print("[OK] Database initialization complete!")


def seed_demo_personas(cursor, conn):
    """Seed three realistic citizen personas for zero-friction hackathon demos."""
    personas = [
        {
            "username": "ramesh_farmer",
            "full_name": "Ramesh Kumar Meena",
            "email": "ramesh.k@demo.jansetu.in",
            "phone": "+91 98765 43210",
            "state": "Rajasthan",
            "district": "Dausa",
            "profile": {
                "age": 42,
                "gender": "Male",
                "occupation": "Farmer",
                "annual_income": 110000,
                "social_category": "ST",
                "marital_status": "Married",
                "is_differently_abled": 0,
                "land_ownership_hectares": 1.4,
                "residence_area": "Rural",
                "family_members_count": 5,
                "is_bpl": 1,
                "raw_attributes_json": json.dumps({
                    "crop_type": "Wheat & Mustard",
                    "irrigation_type": "Tube well",
                    "bank_account_seeded": True
                })
            },
            "documents": [
                {
                    "doc_type": "aadhaar",
                    "doc_name": "Aadhaar Card (Masked Demo)",
                    "ocr": {"aadhaar_masked": "XXXX-XXXX-8921", "holder_name": "Ramesh Kumar Meena", "dob": "1984-05-12", "state": "Rajasthan"}
                },
                {
                    "doc_type": "land_record",
                    "doc_name": "Khasra / Khatauni Land Record (Demo)",
                    "ocr": {"khasra_no": "142/3", "land_area_hectares": 1.4, "owner_name": "Ramesh Kumar Meena", "village": "Lalsot"}
                },
                {
                    "doc_type": "bank_passbook",
                    "doc_name": "SBI Savings Passbook (Demo)",
                    "ocr": {"account_masked": "XXXXXX4920", "ifsc": "SBIN0001234", "bank_name": "State Bank of India", "dbt_enabled": True}
                }
            ]
        },
        {
            "username": "sunita_vendor",
            "full_name": "Sunita Devi",
            "email": "sunita.d@demo.jansetu.in",
            "phone": "+91 98123 45678",
            "state": "Rajasthan",
            "district": "Jaipur",
            "profile": {
                "age": 34,
                "gender": "Female",
                "occupation": "Street Vendor",
                "annual_income": 140000,
                "social_category": "OBC",
                "marital_status": "Married",
                "is_differently_abled": 0,
                "land_ownership_hectares": 0.0,
                "residence_area": "Urban",
                "family_members_count": 4,
                "is_bpl": 1,
                "raw_attributes_json": json.dumps({
                    "vending_type": "Food & Snacks Stall",
                    "vending_location": "Bapu Bazar, Jaipur",
                    "has_cov": True
                })
            },
            "documents": [
                {
                    "doc_type": "aadhaar",
                    "doc_name": "Aadhaar Card (Masked Demo)",
                    "ocr": {"aadhaar_masked": "XXXX-XXXX-4102", "holder_name": "Sunita Devi", "dob": "1992-08-19", "state": "Rajasthan"}
                },
                {
                    "doc_type": "vending_certificate",
                    "doc_name": "Jaipur Nagar Nigam Vending Certificate (Demo)",
                    "ocr": {"cov_no": "JMC-VN-2023-7841", "vendor_name": "Sunita Devi", "ward": "Ward 42, Jaipur", "valid_till": "2027-12-31"}
                },
                {
                    "doc_type": "bank_passbook",
                    "doc_name": "Bank of Baroda Passbook (Demo)",
                    "ocr": {"account_masked": "XXXXXX8912", "ifsc": "BARB0JAIPUR", "dbt_enabled": True}
                }
            ]
        },
        {
            "username": "pooja_student",
            "full_name": "Pooja Sharma",
            "email": "pooja.s@demo.jansetu.in",
            "phone": "+91 97654 32109",
            "state": "Rajasthan",
            "district": "Jaipur",
            "profile": {
                "age": 20,
                "gender": "Female",
                "occupation": "Student",
                "annual_income": 180000,
                "social_category": "EWS",
                "marital_status": "Single",
                "is_differently_abled": 0,
                "land_ownership_hectares": 0.0,
                "residence_area": "Urban",
                "family_members_count": 3,
                "is_bpl": 0,
                "raw_attributes_json": json.dumps({
                    "education_level": "Undergraduate (B.Tech 2nd Year)",
                    "college_name": "Government Engineering College, Jaipur",
                    "merit_percentage": 84.5
                })
            },
            "documents": [
                {
                    "doc_type": "aadhaar",
                    "doc_name": "Aadhaar Card (Masked Demo)",
                    "ocr": {"aadhaar_masked": "XXXX-XXXX-6531", "holder_name": "Pooja Sharma", "dob": "2006-03-14", "state": "Rajasthan"}
                },
                {
                    "doc_type": "income_certificate",
                    "doc_name": "Tehsildar Family Income Certificate (Demo)",
                    "ocr": {"certificate_no": "INC-2025-4512", "annual_family_income": 180000, "issuer": "Tehsildar, Jaipur"}
                },
                {
                    "doc_type": "college_admission_receipt",
                    "doc_name": "College Fee Receipt 2025-26 (Demo)",
                    "ocr": {"enrollment_no": "EN-2023-891", "institution": "Govt Eng College", "academic_year": "2025-26"}
                }
            ]
        }
    ]

    for p in personas:
        # Insert user
        cursor.execute(
            """
            INSERT INTO users (username, full_name, email, phone, state, district)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(username) DO UPDATE SET
                full_name=excluded.full_name,
                email=excluded.email,
                phone=excluded.phone,
                state=excluded.state,
                district=excluded.district
        """,
            (p["username"], p["full_name"], p["email"], p["phone"], p["state"], p["district"]),
        )
        user_id = cursor.lastrowid
        if not user_id:
            cursor.execute("SELECT id FROM users WHERE username = ?", (p["username"],))
            user_id = cursor.fetchone()[0]

        # Insert citizen profile
        prof = p["profile"]
        cursor.execute(
            """
            INSERT INTO citizen_profiles (
                user_id, age, gender, occupation, annual_income, social_category,
                marital_status, is_differently_abled, land_ownership_hectares,
                residence_area, family_members_count, is_bpl, raw_attributes_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                age=excluded.age,
                gender=excluded.gender,
                occupation=excluded.occupation,
                annual_income=excluded.annual_income,
                social_category=excluded.social_category,
                marital_status=excluded.marital_status,
                is_differently_abled=excluded.is_differently_abled,
                land_ownership_hectares=excluded.land_ownership_hectares,
                residence_area=excluded.residence_area,
                family_members_count=excluded.family_members_count,
                is_bpl=excluded.is_bpl,
                raw_attributes_json=excluded.raw_attributes_json
        """,
            (
                user_id,
                prof["age"],
                prof["gender"],
                prof["occupation"],
                prof["annual_income"],
                prof["social_category"],
                prof["marital_status"],
                prof["is_differently_abled"],
                prof["land_ownership_hectares"],
                prof["residence_area"],
                prof["family_members_count"],
                prof["is_bpl"],
                prof["raw_attributes_json"],
            ),
        )

        # Insert user demo documents
        for doc in p["documents"]:
            cursor.execute(
                """
                INSERT INTO user_documents (
                    user_id, doc_type, doc_name, status, verified_ocr_data_json
                ) VALUES (?, ?, ?, 'VERIFIED_DEMO', ?)
            """,
                (user_id, doc["doc_type"], doc["doc_name"], json.dumps(doc["ocr"])),
            )

        # Add initial welcome notification
        cursor.execute(
            """
            INSERT INTO notifications (user_id, title, message, type)
            VALUES (?, ?, ?, 'INFO')
        """,
            (
                user_id,
                "Welcome to JanSetu!",
                f"Namaste {p['full_name']}! Your verified demo citizen profile is ready. You can now discover matching welfare schemes.",
            ),
        )

    conn.commit()
    print("[OK] Successfully seeded 3 realistic citizen personas with demo documents.")


if __name__ == "__main__":
    init_database()
