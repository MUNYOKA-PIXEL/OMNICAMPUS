-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS book_loans;
DROP TABLE IF EXISTS library_books;
DROP TABLE IF EXISTS lost_items;
DROP TABLE IF EXISTS found_items;
DROP TABLE IF EXISTS lost_item_claims;
DROP TABLE IF EXISTS found_item_claims;
DROP TABLE IF EXISTS club_memberships;
DROP TABLE IF EXISTS clubs;
DROP TABLE IF EXISTS club_events;
DROP TABLE IF EXISTS event_rsvps;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS admins;
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS book_requests;
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS medications;
DROP TABLE IF EXISTS prescriptions;
DROP TABLE IF EXISTS prescription_refills;
DROP TABLE IF EXISTS medical_records;

-- Drop module-specific admin tables
DROP TABLE IF EXISTS library_admins;
DROP TABLE IF EXISTS lost_found_admins;
DROP TABLE IF EXISTS clubs_admins;
DROP TABLE IF EXISTS medical_admins;
DROP TABLE IF EXISTS user_admins;

-- Users table (students)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password_hash VARCHAR(255) NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    is_active BOOLEAN DEFAULT 1,
    profile_pic VARCHAR(255)
);

-- Super admins table (full access)
CREATE TABLE admins (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(50) DEFAULT 'super_admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    is_active BOOLEAN DEFAULT 1
);

-- Library admins
CREATE TABLE library_admins (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(50) DEFAULT 'library_admin',
    can_add_books BOOLEAN DEFAULT 1,
    can_edit_books BOOLEAN DEFAULT 1,
    can_delete_books BOOLEAN DEFAULT 0,
    can_manage_loans BOOLEAN DEFAULT 1,
    can_approve_requests BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    is_active BOOLEAN DEFAULT 1
);

-- Lost & Found admins
CREATE TABLE lost_found_admins (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(50) DEFAULT 'lost_found_admin',
    can_verify_items BOOLEAN DEFAULT 1,
    can_approve_claims BOOLEAN DEFAULT 1,
    can_delete_items BOOLEAN DEFAULT 0,
    can_manage_matches BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    is_active BOOLEAN DEFAULT 1
);

-- Clubs admins
CREATE TABLE clubs_admins (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(50) DEFAULT 'clubs_admin',
    can_create_clubs BOOLEAN DEFAULT 1,
    can_edit_clubs BOOLEAN DEFAULT 1,
    can_delete_clubs BOOLEAN DEFAULT 0,
    can_approve_members BOOLEAN DEFAULT 1,
    can_manage_events BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    is_active BOOLEAN DEFAULT 1
);

-- Medical admins
CREATE TABLE medical_admins (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(50) DEFAULT 'medical_admin',
    can_manage_doctors BOOLEAN DEFAULT 1,
    can_manage_appointments BOOLEAN DEFAULT 1,
    can_manage_prescriptions BOOLEAN DEFAULT 1,
    can_manage_records BOOLEAN DEFAULT 0,
    can_manage_medications BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    is_active BOOLEAN DEFAULT 1
);

-- User admins
CREATE TABLE user_admins (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(50) DEFAULT 'user_admin',
    can_view_users BOOLEAN DEFAULT 1,
    can_edit_users BOOLEAN DEFAULT 1,
    can_delete_users BOOLEAN DEFAULT 0,
    can_create_admins BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    is_active BOOLEAN DEFAULT 1
);

-- Library books
CREATE TABLE library_books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    category VARCHAR(50),
    publication_year INTEGER,
    publisher VARCHAR(100),
    total_copies INTEGER DEFAULT 1,
    available_copies INTEGER DEFAULT 1,
    shelf_location VARCHAR(50),
    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    added_by INTEGER,
    cover_image VARCHAR(255),
    FOREIGN KEY (added_by) REFERENCES library_admins(id)
);

-- Book loans
CREATE TABLE book_loans (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date DATETIME NOT NULL,
    return_date DATETIME,
    fine_amount DECIMAL(10,2) DEFAULT 0,
    fine_paid BOOLEAN DEFAULT 0,
    status VARCHAR(20) DEFAULT 'issued',
    issued_by INTEGER,
    returned_to INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES library_books(id),
    FOREIGN KEY (issued_by) REFERENCES library_admins(id),
    FOREIGN KEY (returned_to) REFERENCES library_admins(id)
);

-- Book requests
CREATE TABLE book_requests (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    book_title VARCHAR(200) NOT NULL,
    book_author VARCHAR(100),
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    processed_by INTEGER,
    processed_date DATETIME,
    admin_notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (processed_by) REFERENCES library_admins(id)
);

-- Lost items
CREATE TABLE lost_items (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    location_lost VARCHAR(100),
    date_lost DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'lost',
    image_url VARCHAR(255),
    reported_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified_by INTEGER,
    verified_date DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (verified_by) REFERENCES lost_found_admins(id)
);

-- Found items
CREATE TABLE found_items (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    location_found VARCHAR(100),
    date_found DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'found',
    image_url VARCHAR(255),
    reported_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified_by INTEGER,
    verified_date DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (verified_by) REFERENCES lost_found_admins(id)
);

-- Lost item claims
CREATE TABLE lost_item_claims (
    id SERIAL PRIMARY KEY,
    lost_item_id INTEGER NOT NULL,
    claimer_id INTEGER NOT NULL,
    claim_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    admin_notes TEXT,
    processed_by INTEGER,
    processed_date DATETIME,
    FOREIGN KEY (lost_item_id) REFERENCES lost_items(id),
    FOREIGN KEY (claimer_id) REFERENCES users(id),
    FOREIGN KEY (processed_by) REFERENCES lost_found_admins(id)
);

-- Found item claims
CREATE TABLE found_item_claims (
    id SERIAL PRIMARY KEY,
    found_item_id INTEGER NOT NULL,
    claimant_id INTEGER NOT NULL,
    claim_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    admin_notes TEXT,
    processed_by INTEGER,
    processed_date DATETIME,
    FOREIGN KEY (found_item_id) REFERENCES found_items(id),
    FOREIGN KEY (claimant_id) REFERENCES users(id),
    FOREIGN KEY (processed_by) REFERENCES lost_found_admins(id)
);

-- Clubs
CREATE TABLE clubs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    category VARCHAR(50),
    president_id INTEGER,
    vice_president_id INTEGER,
    treasurer_id INTEGER,
    secretary_id INTEGER,
    meeting_schedule VARCHAR(200),
    contact_email VARCHAR(100),
    contact_phone VARCHAR(20),
    logo_url VARCHAR(255),
    established_date DATE,
    dues_amount DECIMAL(10,2) DEFAULT 0,
    members INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active',
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_by INTEGER,
    approved_date DATETIME,
    FOREIGN KEY (president_id) REFERENCES users(id),
    FOREIGN KEY (vice_president_id) REFERENCES users(id),
    FOREIGN KEY (treasurer_id) REFERENCES users(id),
    FOREIGN KEY (secretary_id) REFERENCES users(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (approved_by) REFERENCES clubs_admins(id)
);

-- Club memberships
CREATE TABLE club_memberships (
    id SERIAL PRIMARY KEY,
    club_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    role VARCHAR(50) DEFAULT 'member',
    joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    dues_paid BOOLEAN DEFAULT 0,
    dues_amount DECIMAL(10,2) DEFAULT 0,
    dues_paid_date DATETIME,
    status VARCHAR(20) DEFAULT 'active',
    approved_by INTEGER,
    approved_date DATETIME,
    FOREIGN KEY (club_id) REFERENCES clubs(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (approved_by) REFERENCES clubs_admins(id),
    UNIQUE(club_id, user_id)
);

-- Club events
CREATE TABLE club_events (
    id SERIAL PRIMARY KEY,
    club_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    event_date DATETIME NOT NULL,
    location VARCHAR(100),
    max_participants INTEGER,
    current_participants INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'upcoming',
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_by INTEGER,
    approved_date DATETIME,
    FOREIGN KEY (club_id) REFERENCES clubs(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (approved_by) REFERENCES clubs_admins(id)
);

-- Event RSVPs
CREATE TABLE event_rsvps (
    id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    rsvp_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'confirmed',
    attended BOOLEAN DEFAULT 0,
    FOREIGN KEY (event_id) REFERENCES club_events(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(event_id, user_id)
);

-- Doctors
CREATE TABLE doctors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    available BOOLEAN DEFAULT 1,
    education TEXT,
    experience VARCHAR(50),
    languages TEXT,
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    FOREIGN KEY (created_by) REFERENCES medical_admins(id)
);

-- Appointments
CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    service_type VARCHAR(100) NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time VARCHAR(10) NOT NULL,
    reason TEXT,
    status VARCHAR(20) DEFAULT 'upcoming',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    cancelled_by INTEGER,
    cancelled_date DATETIME,
    cancellation_reason TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id),
    FOREIGN KEY (created_by) REFERENCES medical_admins(id),
    FOREIGN KEY (cancelled_by) REFERENCES medical_admins(id)
);

-- Medications
CREATE TABLE medications (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    price DECIMAL(10,2) NOT NULL,
    stock INTEGER DEFAULT 0,
    requires_prescription BOOLEAN DEFAULT 1,
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by INTEGER,
    updated_at DATETIME,
    FOREIGN KEY (created_by) REFERENCES medical_admins(id),
    FOREIGN KEY (updated_by) REFERENCES medical_admins(id)
);

-- Prescriptions
CREATE TABLE prescriptions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    medication_id INTEGER NOT NULL,
    dosage VARCHAR(100) NOT NULL,
    instructions TEXT,
    prescribed_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    refills INTEGER DEFAULT 0,
    refills_used INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active',
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id),
    FOREIGN KEY (medication_id) REFERENCES medications(id),
    FOREIGN KEY (created_by) REFERENCES medical_admins(id)
);

-- Prescription refills
CREATE TABLE prescription_refills (
    id SERIAL PRIMARY KEY,
    prescription_id INTEGER NOT NULL,
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    approved_by INTEGER,
    approved_date DATETIME,
    FOREIGN KEY (prescription_id) REFERENCES prescriptions(id),
    FOREIGN KEY (approved_by) REFERENCES medical_admins(id)
);

-- Medical records
CREATE TABLE medical_records (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    record_type VARCHAR(50) NOT NULL,
    record_date DATE NOT NULL,
    doctor_id INTEGER NOT NULL,
    diagnosis TEXT,
    notes TEXT,
    attachments TEXT,
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id),
    FOREIGN KEY (created_by) REFERENCES medical_admins(id)
);

-- Feedback
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    category VARCHAR(50),
    message TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'new',
    admin_response TEXT,
    responded_by INTEGER,
    responded_date DATETIME,
    submitted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (responded_by) REFERENCES admins(id)
);

-- Insert default super admin (password: admin123)
-- Hash for 'admin123' is: 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918
INSERT INTO admins (username, email, password_hash, full_name, role, is_active) VALUES 
('superadmin', 'superadmin@omnicampus.edu', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'Super Administrator', 'super_admin', 1);

-- Insert module-specific admins (all passwords: admin123)
INSERT INTO library_admins (username, password_hash, full_name, email, phone, is_active) VALUES 
('libadmin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'Library Admin', 'library@omnicampus.edu', '254700111222', 1);

INSERT INTO lost_found_admins (username, password_hash, full_name, email, phone, is_active) VALUES 
('lfadmin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'Lost & Found Admin', 'lostfound@omnicampus.edu', '254700111333', 1);

INSERT INTO clubs_admins (username, password_hash, full_name, email, phone, is_active) VALUES 
('clubsadmin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'Clubs Admin', 'clubs@omnicampus.edu', '254700111444', 1);

INSERT INTO medical_admins (username, password_hash, full_name, email, phone, is_active) VALUES 
('medadmin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'Medical Admin', 'medical@omnicampus.edu', '254700111555', 1);

INSERT INTO user_admins (username, password_hash, full_name, email, phone, is_active) VALUES 
('useradmin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'User Admin', 'users@omnicampus.edu', '254700111666', 1);

-- Insert sample students (password: password123)
-- Hash for 'password123' is: 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918
INSERT INTO users (student_id, first_name, last_name, email, phone, password_hash, is_active) VALUES
('S1001', 'John', 'Doe', 'john.doe@student.edu', '254700111001', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 1),
('S1002', 'Jane', 'Smith', 'jane.smith@student.edu', '254700111002', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 1),
('S1003', 'Mike', 'Johnson', 'mike.johnson@student.edu', '254700111003', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 1);

-- Insert sample library books
INSERT INTO library_books (title, author, isbn, category, total_copies, available_copies) VALUES
('Introduction to Algorithms', 'Thomas H. Cormen', '978-0262033848', 'Computer Science', 5, 5),
('Clean Code', 'Robert C. Martin', '978-0132350884', 'Programming', 3, 3),
('The Pragmatic Programmer', 'David Thomas', '978-0201616224', 'Programming', 4, 4),
('Design Patterns', 'Erich Gamma', '978-0201633610', 'Software Engineering', 2, 2),
('Database System Concepts', 'Abraham Silberschatz', '978-0078022159', 'Computer Science', 3, 3);

-- Insert sample doctors
INSERT INTO doctors (name, specialty, email, phone, available, education, experience, languages) VALUES
('Dr. Sarah Johnson', 'General Medicine', 'sarah.johnson@omnicampus.edu', '254700111777', 1, 'MD, University of Nairobi', '10 years', '["English", "Swahili"]'),
('Dr. Michael Chen', 'Dentistry', 'michael.chen@omnicampus.edu', '254700111778', 1, 'DDS, University of Nairobi', '8 years', '["English", "Mandarin"]'),
('Dr. Emily Brown', 'Counseling', 'emily.brown@omnicampus.edu', '254700111779', 1, 'PhD, Clinical Psychology', '12 years', '["English", "French"]');

-- Insert sample clubs
INSERT INTO clubs (name, description, category, contact_email, dues_amount, members, status) VALUES
('DevClub', 'Software development and coding club', 'Technology', 'devclub@omnicampus.edu', 500, 45, 'active'),
('Business Club', 'Entrepreneurship and business networking', 'Business', 'business@omnicampus.edu', 300, 32, 'active'),
('AI/ML Society', 'Artificial Intelligence and Machine Learning', 'Technology', 'aiml@omnicampus.edu', 400, 28, 'active');

-- Insert sample medications
INSERT INTO medications (name, description, category, price, stock, requires_prescription) VALUES
('Paracetamol 500mg', 'Pain relief and fever reduction', 'Pain Relief', 50, 100, 0),
('Amoxicillin 250mg', 'Antibiotic for bacterial infections', 'Antibiotics', 120, 50, 1),
('Loratadine 10mg', 'Allergy relief', 'Allergy', 80, 75, 0),
('Ibuprofen 400mg', 'Anti-inflammatory pain relief', 'Pain Relief', 65, 60, 0),
('Vitamin C 1000mg', 'Immune system support', 'Supplements', 150, 200, 0);LUES
('Paracetamol 500mg', 'Pain relief and fever reduction', 'Pain Relief', 50, 100, 0),
('Amoxicillin 250mg', 'Antibiotic for bacterial infections', 'Antibiotics', 120, 50, 1),
('Loratadine 10mg', 'Allergy relief', 'Allergy', 80, 75, 0),
('Ibuprofen 400mg', 'Anti-inflammatory pain relief', 'Pain Relief', 65, 60, 0),
('Vitamin C 1000mg', 'Immune system support', 'Supplements', 150, 200, 0);