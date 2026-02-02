

-- Clean up existing data (optional, be careful in production)
TRUNCATE TABLE phones, organization_industries, organizations, buildings, industries RESTART IDENTITY CASCADE;

-- Insert Industries
-- Root Level
INSERT INTO industries (id, name, parent_id, created_at, updated_at) VALUES 
(1, 'Food', NULL, NOW(), NOW()),
(2, 'Technology', NULL, NOW(), NOW()),
(3, 'Healthcare', NULL, NOW(), NOW());

-- Level 2
INSERT INTO industries (id, name, parent_id, created_at, updated_at) VALUES 
(4, 'Restaurants', 1, NOW(), NOW()),
(5, 'Groceries', 1, NOW(), NOW()),
(6, 'Software', 2, NOW(), NOW()),
(7, 'Hardware', 2, NOW(), NOW());

-- Level 3
INSERT INTO industries (id, name, parent_id, created_at, updated_at) VALUES 
(8, 'Sushi', 4, NOW(), NOW()),
(9, 'Pizza', 4, NOW(), NOW()),
(10, 'AI Development', 6, NOW(), NOW());

-- Insert Buildings
-- Coordinates are roughly around a city center (e.g., London/NY/Random) - using Lat/Lon
-- Using ST_GeomFromText('POINT(lon lat)', 4326)
INSERT INTO buildings (id, address, coordinates, created_at, updated_at) VALUES 
(1, '123 Tech Blvd', ST_GeomFromText('POINT(-73.935242 40.730610)', 4326), NOW(), NOW()),
(2, '456 Food St', ST_GeomFromText('POINT(-73.945242 40.740610)', 4326), NOW(), NOW()),
(3, '789 Health Ave', ST_GeomFromText('POINT(-73.955242 40.750610)', 4326), NOW(), NOW()),
(4, '101 Market Rd', ST_GeomFromText('POINT(-73.965242 40.760610)', 4326), NOW(), NOW());


-- Insert Organizations
INSERT INTO organizations (id, name, building_id, created_at, updated_at) VALUES 
(1, 'TechCorp Solutions', 1, NOW(), NOW()),
(2, 'Sushi Master', 2, NOW(), NOW()),
(3, 'Fresh Grocer', 2, NOW(), NOW()),
(4, 'DeepMind AI', 1, NOW(), NOW()),
(5, 'General Hospital', 3, NOW(), NOW());


-- Insert Organization Industries (Many-to-Many)
-- TechCorp -> Software
INSERT INTO organization_industries (organization_id, industry_id, created_at) VALUES (1, 6, NOW());
-- Sushi Master -> Sushi, Restaurants
INSERT INTO organization_industries (organization_id, industry_id, created_at) VALUES (2, 8, NOW());
INSERT INTO organization_industries (organization_id, industry_id, created_at) VALUES (2, 4, NOW());
-- Fresh Grocer -> Groceries
INSERT INTO organization_industries (organization_id, industry_id, created_at) VALUES (3, 5, NOW());
-- DeepMind AI -> AI Development, Software, Technology
INSERT INTO organization_industries (organization_id, industry_id, created_at) VALUES (4, 10, NOW());
INSERT INTO organization_industries (organization_id, industry_id, created_at) VALUES (4, 6, NOW());
INSERT INTO organization_industries (organization_id, industry_id, created_at) VALUES (4, 2, NOW());
-- General Hospital -> Healthcare
INSERT INTO organization_industries (organization_id, industry_id, created_at) VALUES (5, 3, NOW());


-- Insert Phones
INSERT INTO phones (id, organization_id, phone_number, created_at, updated_at) VALUES 
(1, 1, '+1-555-0101', NOW(), NOW()),
(2, 1, '+1-555-0102', NOW(), NOW()),
(3, 2, '+1-555-0201', NOW(), NOW()),
(4, 3, '+1-555-0301', NOW(), NOW()),
(5, 4, '+1-555-0401', NOW(), NOW()),
(6, 5, '+1-555-0501', NOW(), NOW()),
(7, 5, '+1-555-0502', NOW(), NOW());
