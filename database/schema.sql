-- JanSetu (जनसेतु) Relational Schema for SQLite

PRAGMA foreign_keys = ON;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    state TEXT DEFAULT 'Rajasthan',
    district TEXT DEFAULT 'Jaipur',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Citizen Profiles Table
CREATE TABLE IF NOT EXISTS citizen_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    age INTEGER DEFAULT 35,
    gender TEXT DEFAULT 'Male',
    occupation TEXT DEFAULT 'Street Vendor',
    annual_income REAL DEFAULT 120000,
    social_category TEXT DEFAULT 'OBC',
    marital_status TEXT DEFAULT 'Married',
    is_differently_abled INTEGER DEFAULT 0,
    land_ownership_hectares REAL DEFAULT 0.0,
    residence_area TEXT DEFAULT 'Urban',
    family_members_count INTEGER DEFAULT 4,
    is_bpl INTEGER DEFAULT 0,
    raw_attributes_json TEXT DEFAULT '{}',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. Schemes Table
CREATE TABLE IF NOT EXISTS schemes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    name_hindi TEXT,
    ministry TEXT NOT NULL,
    category TEXT NOT NULL,
    target_audience TEXT,
    short_description TEXT NOT NULL,
    full_description TEXT,
    benefits TEXT NOT NULL,
    max_benefit_amount REAL DEFAULT 0,
    eligibility_criteria_json TEXT NOT NULL,
    required_documents_json TEXT NOT NULL,
    application_process TEXT,
    official_url TEXT,
    level TEXT DEFAULT 'Central',
    state TEXT DEFAULT 'All India',
    verification_date TEXT DEFAULT 'unknown',
    source TEXT DEFAULT 'myScheme / Official Department Portal',
    tags TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. User Demo Documents Table
CREATE TABLE IF NOT EXISTS user_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    doc_type TEXT NOT NULL,
    doc_name TEXT NOT NULL,
    file_path TEXT,
    file_size INTEGER DEFAULT 1024,
    status TEXT DEFAULT 'VERIFIED_DEMO',
    verified_ocr_data_json TEXT DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 5. Applications Table (Simulated Workflow)
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reference_no TEXT UNIQUE NOT NULL,
    user_id INTEGER NOT NULL,
    scheme_id INTEGER NOT NULL,
    status TEXT DEFAULT 'SUBMITTED',
    applicant_data_json TEXT NOT NULL,
    eligibility_answers_json TEXT DEFAULT '[]',
    draft_summary TEXT NOT NULL,
    user_approved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estimated_resolution_date TEXT,
    tracking_history_json TEXT NOT NULL,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (scheme_id) REFERENCES schemes(id) ON DELETE CASCADE
);

-- 6. Notifications Table
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    application_id INTEGER,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    type TEXT DEFAULT 'INFO',
    is_read INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE SET NULL
);

-- 7. Chat History Table
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    user_id INTEGER,
    sender TEXT NOT NULL,
    message TEXT NOT NULL,
    metadata_json TEXT DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for efficient queries
CREATE INDEX IF NOT EXISTS idx_schemes_category ON schemes(category);
CREATE INDEX IF NOT EXISTS idx_schemes_code ON schemes(code);
CREATE INDEX IF NOT EXISTS idx_schemes_level ON schemes(level);
CREATE INDEX IF NOT EXISTS idx_schemes_state ON schemes(state);
CREATE INDEX IF NOT EXISTS idx_applications_user ON applications(user_id);
CREATE INDEX IF NOT EXISTS idx_applications_ref ON applications(reference_no);
CREATE INDEX IF NOT EXISTS idx_user_documents_user ON user_documents(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_session ON chat_history(session_id);
