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
    user_favorite BOOLEAN DEFAULT FALSE,
    product_id INT UNSIGNED NOT NULL,
    
    PRIMARY KEY (id),
    INDEX ind_product_id(product_id),
    INDEX ind_user_favorite(user_favorite)
);

ALTER TABLE Product 
ADD CONSTRAINT fk_category_id FOREIGN KEY (category_id) REFERENCES Category(id);

ALTER TABLE OffData 
ADD CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES Product(id);