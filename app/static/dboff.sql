DROP DATABASE IF EXISTS offdb;
CREATE DATABASE offdb CHARACTER SET 'utf8';
USE offdb;

CREATE TABLE Category (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(50),
    PRIMARY KEY (id)
);

CREATE TABLE Product (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(50),
    category_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE OffData(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    product_name VARCHAR(255),
    brands VARCHAR(255),
    quantity VARCHAR(255),
    stores VARCHAR(255),
    url VARCHAR(255),
    nutrition_grades VARCHAR(1),
    product_id INT UNSIGNED NOT NULL,
    
    PRIMARY KEY (id),
    INDEX ind_product_id(product_id)
);

CREATE TABLE Substitute(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    origin_id INT UNSIGNED NOT NULL,
    substitute_id INT UNSIGNED NOT NULL,

    PRIMARY KEY (id),
    INDEX ind_origin_id(origin_id)
);

ALTER TABLE Product 
ADD CONSTRAINT fk_category_id FOREIGN KEY (category_id) REFERENCES Category(id) ON DELETE CASCADE;

ALTER TABLE OffData 
ADD CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES Product(id) ON DELETE CASCADE;

ALTER TABLE Substitute
ADD CONSTRAINT fk_origin_id FOREIGN KEY (origin_id) REFERENCES OffData(id) ON DELETE CASCADE;
ALTER TABLE Substitute
ADD CONSTRAINT fk_substitute_id FOREIGN KEY (substitute_id) REFERENCES OffData(id) ON DELETE CASCADE;

CREATE VIEW V_Substitute AS
SELECT 
Substitute.id as id,
Category.name as category,
Product.name as product_type,
origin_id,
CONCAT(OD_origin.product_name," - ",OD_origin.brands, " - ", OD_origin.quantity) as origin_designation,
substitute_id,
CONCAT(OD_substitute.product_name," - ",OD_substitute.brands, " - ", OD_substitute.quantity) as substitute_designation
FROM `Substitute` 
JOIN OffData OD_origin ON origin_id = OD_origin.id
JOIN OffData OD_substitute ON substitute_id = OD_substitute.id
JOIN Product ON Product.id = OD_origin.product_id
JOIN Category ON Category.id = Product.category_id