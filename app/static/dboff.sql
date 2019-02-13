DROP DATABASE IF EXISTS offdb;
--
CREATE DATABASE offdb CHARACTER SET 'utf8';
--
USE offdb;
--
CREATE TABLE Category (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(50),
    PRIMARY KEY (id)
);
--
CREATE TABLE Product(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    product_name VARCHAR(255),
    brands VARCHAR(255),
    quantity VARCHAR(255),
    stores VARCHAR(255),
    url VARCHAR(255),
    nutrition_grades VARCHAR(1),
    category_id INT UNSIGNED NOT NULL,
    
    PRIMARY KEY (id),
    INDEX ind_category_id(category_id)
);
--
CREATE TABLE Substitute(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    origin_id INT UNSIGNED NOT NULL,
    substitute_id INT UNSIGNED NOT NULL,

    PRIMARY KEY (id),
    INDEX ind_origin_id(origin_id)
);
--
ALTER TABLE Product 
ADD CONSTRAINT fk_category_id FOREIGN KEY (category_id) REFERENCES Category(id) ON DELETE CASCADE;
--
ALTER TABLE Substitute
ADD CONSTRAINT fk_origin_id FOREIGN KEY (origin_id) REFERENCES Product(id) ON DELETE CASCADE;
--
ALTER TABLE Substitute
ADD CONSTRAINT fk_substitute_id FOREIGN KEY (substitute_id) REFERENCES Product(id) ON DELETE CASCADE;
--
ALTER TABLE Substitute ADD UNIQUE(origin_id, substitute_id);
--
CREATE VIEW V_Substitute AS
SELECT 
Substitute.id as id,
Category.name as category,
origin_id,
CONCAT(OD_origin.product_name," - ",OD_origin.brands, " - ", OD_origin.quantity) as origin_designation,
substitute_id,
CONCAT(OD_substitute.product_name," - ",OD_substitute.brands, " - ", OD_substitute.quantity) as substitute_designation
FROM `Substitute` 
JOIN Product OD_origin ON origin_id = OD_origin.id
JOIN Product OD_substitute ON substitute_id = OD_substitute.id
JOIN Category ON Category.id = OD_origin.category_id;
--
CREATE PROCEDURE get_better_product (IN p_id_product INT) 
BEGIN 
    SELECT * FROM `Product` 
    WHERE category_id=(
        SELECT category_id FROM Product WHERE id = p_id_product
        )
    AND id <> p_id_product
    AND `nutrition_grades` <= (
        SELECT IFNULL(
            (SELECT nutrition_grades 
            FROM Product WHERE id = p_id_product),
        'z')
        )
    AND `nutrition_grades` <> ''
    ORDER BY `nutrition_grades`; 
END
--
CREATE PROCEDURE show_details (IN p_origin_id INT, IN p_substitute_id INT)
BEGIN
    SELECT 
    CONCAT(OD_origin.product_name," - ",OD_origin.brands, " - ", OD_origin.quantity) as origin_designation,
    OD_origin.nutrition_grades as origin_grade,
    CONCAT(OD_substitute.product_name," - ",OD_substitute.brands, " - ", OD_substitute.quantity) as substitute_designation,
    OD_substitute.nutrition_grades as substitute_grade,
    OD_substitute.url as url,
    OD_substitute.stores as stores,
    (SELECT id FROM Substitute WHERE origin_id = p_origin_id AND substitute_id = p_substitute_id) as substitute_exist
    FROM `Product` 
    JOIN Product OD_origin ON OD_origin.id = p_origin_id
    JOIN Product OD_substitute ON OD_substitute.id = p_substitute_id
    LIMIT 1;
END
--