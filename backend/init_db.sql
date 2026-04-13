-- QUAN HO BAC NINH - DATABASE SETUP SCRIPT (SQLITE COMPATIBLE)

-- 1. DROP TABLES IF EXISTS (Reverse order of dependencies)
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS media;
DROP TABLE IF EXISTS event_registrations;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS histories;
DROP TABLE IF EXISTS favorites;
DROP TABLE IF EXISTS articles;
DROP TABLE IF EXISTS melodies;
DROP TABLE IF EXISTS artists;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS users;

-- 2. CREATE TABLES

-- Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    phone VARCHAR(20),
    bio TEXT,
    avatar_url VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Artists Table
CREATE TABLE artists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE,
    birth_year INTEGER,
    death_year INTEGER,
    description TEXT,
    biography TEXT,
    contributions TEXT,
    performances INTEGER DEFAULT 0,
    image_url VARCHAR(500),
    village VARCHAR(255),
    achievements TEXT,
    generation VARCHAR(50) DEFAULT 'truyen-thong',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Locations Table (Villages)
CREATE TABLE locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE,
    address TEXT,
    latitude FLOAT,
    longitude FLOAT,
    district VARCHAR(255),
    artist_count INTEGER DEFAULT 0,
    featured_songs TEXT,
    badges TEXT,
    description TEXT,
    history TEXT,
    culture TEXT,
    festival VARCHAR(255),
    image_url VARCHAR(500),
    type VARCHAR(50) DEFAULT 'lang-quan-ho',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Melodies Table
CREATE TABLE melodies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE,
    description TEXT,
    lyrics TEXT,
    audio_url VARCHAR(500),
    video_url VARCHAR(500),
    category VARCHAR(50) DEFAULT 'co',
    village VARCHAR(255),
    difficulty VARCHAR(50) DEFAULT 'trung-binh',
    image_url VARCHAR(500),
    duration VARCHAR(50),
    artist_id INTEGER,
    views INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (artist_id) REFERENCES artists(id)
);

-- Articles Table (News/History)
CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(500) NOT NULL,
    slug VARCHAR(500) UNIQUE,
    content TEXT,
    excerpt TEXT,
    image_url VARCHAR(500),
    category VARCHAR(50) DEFAULT 'tin-tuc',
    views INTEGER DEFAULT 0,
    status VARCHAR(50) DEFAULT 'draft',
    author_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users(id)
);

-- Events Table
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(500) NOT NULL,
    slug VARCHAR(500) UNIQUE,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE,
    location_id INTEGER,
    image_url VARCHAR(500),
    status VARCHAR(50) DEFAULT 'upcoming',
    max_participants INTEGER DEFAULT 100,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

-- Comments Table
CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    melody_id INTEGER,
    article_id INTEGER,
    parent_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (melody_id) REFERENCES melodies(id) ON DELETE CASCADE,
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES comments(id) ON DELETE CASCADE
);

-- 3. INSERT SAMPLE DATA

-- Admin User (Password: admin123 - hashed)
INSERT INTO users (name, email, hashed_password, role) 
VALUES ('Quan Tri Vien', 'admin@quanho.vn', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGGa31lW', 'admin');

-- Sample Artist
INSERT INTO artists (name, slug, birth_year, description, village, generation, image_url)
VALUES ('Nghe nhan Thuy Cai', 'thuy-cai', 1955, 'Mot trong nhung nghe nhan gao coi cua lang Quan ho Viem Xa.', 'Viem Xa', 'truyen-thong', '/static/artists/thuy_cai.png');

-- Sample Location (Village)
INSERT INTO locations (name, slug, address, district, latitude, longitude, artist_count, description, image_url)
VALUES ('Lang Viem Xa (Diềm)', 'lang-diem', 'Xa Hoa Long, TP Bac Ninh', 'TP Bac Ninh', 21.2136, 106.0763, 15, 'Coi nguon cua Dan ca Quan ho Bac Ninh.', '/static/news/hoi_lim.png');

-- Sample Melody
INSERT INTO melodies (name, slug, description, category, artist_id, video_url, image_url)
VALUES ('Gia Ban', 'gia-ban', 'Mot trong nhung bai hat quan ho co dac sac nhat.', 'co', 1, 'https://www.youtube.com/watch?v=5U7z0Zc8B2A', '/static/gallery/gallery_1.png');

-- Sample Article
INSERT INTO articles (title, slug, content, excerpt, category, status, image_url)
VALUES ('Nghe thuat thuong thuc Quan ho', 'nghe-thuat-thuong-thuc', 'Noi dung chi tiet ve cach nghe va hieu Quan ho.', 'Huong dan cach thuong thuc Quan ho cho nguoi moi.', 'nghe_thuat', 'published', '/static/news/hat_tren_thuyen.png');
