CREATE TYPE user_role AS ENUM ('ADMIN', 'MANAGER', 'USER');

CREATE TABLE "user" (
id SERIAL PRIMARY KEY,
is_active BOOLEAN DEFAULT TRUE,
username VARCHAR(255),
email VARCHAR(255) UNIQUE,
role user_role DEFAULT 'USER',
hashed_password VARCHAR(255),
balance INTEGER DEFAULT 0
);

CREATE TYPE transaction_payment_type AS ENUM ('PLUS', 'MINUS');
CREATE TYPE transaction_access AS ENUM ('CONFIRMED', 'REJECTED');

CREATE TABLE transaction (
id SERIAL PRIMARY KEY,
user_id INTEGER REFERENCES "user" (id),
payment INTEGER DEFAULT 0,
payment_type transaction_payment_type,
description TEXT,
access transaction_access,
datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (user_id) REFERENCES "user" (id)
);

CREATE TABLE performance (
id SERIAL PRIMARY KEY,
name VARCHAR(255),
description TEXT,
date DATE,
time TIME
);

CREATE TABLE ticket (
id SERIAL PRIMARY KEY,
price INTEGER,
place_number INTEGER,
row_number INTEGER,
performance_id INTEGER REFERENCES performance (id),
owner_id INTEGER REFERENCES "user" (id),
FOREIGN KEY (performance_id) REFERENCES performance (id),
FOREIGN KEY (owner_id) REFERENCES "user" (id)
);

-- Создание индексов

CREATE UNIQUE INDEX ix_user_email ON "user" (email);

-- Создание функций

CREATE FUNCTION set_transaction_datetime()
RETURNS TRIGGER AS $$
BEGIN
NEW.datetime = NOW();
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Создание триггеров

CREATE TRIGGER transaction_datetime_trigger
BEFORE INSERT OR UPDATE
ON transaction
FOR EACH ROW
EXECUTE FUNCTION set_transaction_datetime();

-- Создание пользователя admin

INSERT INTO "user" (is_active, username, email, role, hashed_password, balance)
VALUES (TRUE, 'admin', 'admin@example.com', 'ADMIN', '$2b$12$Aolc8CFOr7CE/ceG4ckHyOYhcp6ExigZ2QH.8bnuNh7JIQgHMFxri', 0);

-- Создание спектаклей

INSERT INTO performance (name, description, date, time)
VALUES
    ('Сказки Хана-Гана', 'Детский спектакль', '2023-06-01', '15:00'),
    ('Вечер в опере', 'Оперный спектакль', '2023-06-05', '18:00'),
    ('Красавица и чудовище', 'Мюзикл', '2023-06-10', '19:00'),
    ('Ромео и Джульетта', 'Балет', '2023-06-15', '20:00');

-- Создание билетов

INSERT INTO ticket (price, place_number, row_number, performance_id, owner_id)
VALUES
    (1000, 1, 1, 1, NULL),
    (1000, 2, 1, 1, NULL),
    (1000, 3, 1, 1, NULL),
    (1500, 1, 2, 1, NULL),
    (1500, 2, 2, 1, NULL),
    (2000, 1, 1, 2, NULL),
    (2000, 2, 1, 2, NULL),
    (2000, 3, 1, 2, NULL),
    (2500, 1, 2, 2, NULL),
    (2500, 2, 2, 2, NULL),
    (3000, 1, 1, 3, NULL),
    (3000, 2, 1, 3, NULL),
    (3000, 3, 1, 3, NULL),
    (3500, 1, 2, 3, NULL),
    (3500, 2, 2, 3, NULL),
    (4000, 1, 1, 4, NULL),
    (4000, 2, 1, 4, NULL),
    (4000, 3, 1, 4, NULL),
    (4500, 1, 2, 4, NULL),
    (4500, 2, 2, 4, NULL);
