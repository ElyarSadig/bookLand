
-- User table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL,
    registration_date TIMESTAMP NOT NULL,
    last_login_date TIMESTAMP,
    is_publisher BOOLEAN NOT NULL,
    phone_number VARCHAR(11) UNIQUE,
    phone_number2 VARCHAR(11),
    address VARCHAR(255),
    identity_image VARCHAR(255),
    card_number VARCHAR(50),
    publications_name VARCHAR(255) UNIQUE,
    publications_image VARCHAR(255),
    is_confirm BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS user_activity_codes (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    activation_code VARCHAR(6),
    created_date TIMESTAMP,
    expire_date TIMESTAMP
);

-- Role table
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    role VARCHAR(50) UNIQUE,
    description VARCHAR(150)
);

-- UserRole table
CREATE TABLE IF NOT EXISTS user_roles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    role_id INTEGER REFERENCES roles(id),
    UNIQUE(user_id, role_id)
);

-- Language table
CREATE TABLE IF NOT EXISTS languages (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE
);

-- Book table
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),      -- Publisher
    book_name VARCHAR(255) NOT NULL,
    author_name VARCHAR(255) NOT NULL,
    translator_name VARCHAR(255),
    released_date INTEGER NOT NULL,
    book_cover_image VARCHAR(255),
    price INTEGER NOT NULL,
    description TEXT,
    number_of_pages INTEGER,
    language_id INTEGER REFERENCES languages(id),
    is_delete BOOLEAN NOT NULL,
    demo_file VARCHAR(255) NOT NULL,
    original_file VARCHAR(255) NOT NULL,
    created_date_time TIMESTAMP
);

-- Review table
CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    book_id INTEGER REFERENCES books(id),
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    created_at TIMESTAMP
);

-- UserBooks table
CREATE TABLE IF NOT EXISTS user_books (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books(id),
    user_id INTEGER REFERENCES users(id),
    bought_time TIMESTAMP
);

-- UserBookmarks table
CREATE TABLE IF NOT EXISTS user_bookmarks (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books(id),
    user_id INTEGER REFERENCES users(id),
    added_time TIMESTAMP,
    is_delete BOOLEAN,
    CONSTRAINT unique_user_bookmark UNIQUE (user_id, book_id)
);

-- Comments table
CREATE TABLE IF NOT EXISTS comments (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books(id),
    user_id INTEGER REFERENCES users(id),
    comment TEXT,
    is_delete BOOLEAN,
    created_date TIMESTAMP
);

-- Category table
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);

-- BookCategory table
CREATE TABLE IF NOT EXISTS book_categories (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id),
    book_id INTEGER REFERENCES books(id),
    is_delete BOOLEAN
);

-- WalletActionType table
CREATE TABLE IF NOT EXISTS wallet_action_types (
    id SERIAL PRIMARY KEY,
    action_type VARCHAR(255) UNIQUE
);

-- WalletAction table
CREATE TABLE IF NOT EXISTS wallet_actions (
    id SERIAL PRIMARY KEY,
    action_type_id INTEGER REFERENCES wallet_action_types(Id),
    user_id INTEGER REFERENCES users(Id),
    amount INTEGER,
    is_successful BOOLEAN,
    description VARCHAR(255),
    created_date TIMESTAMP
);

-- Discount table
CREATE TABLE IF NOT EXISTS discounts (
    id SERIAL PRIMARY KEY,
    code VARCHAR(255) UNIQUE,
    quantity INTEGER,
    percent DECIMAL(4,2),
    created_date TIMESTAMP,
    expire_date TIMESTAMP,
    is_delete BOOLEAN
);

-- UserDiscounts table
CREATE TABLE IF NOT EXISTS user_discounts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    discount_id INTEGER REFERENCES discounts(id)
);
