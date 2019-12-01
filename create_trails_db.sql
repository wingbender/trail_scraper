DROP DATABASE IF EXISTS `trails`;
CREATE DATABASE `trails`;
USE `trails`;

DROP TABLE IF EXISTS `trails`;
CREATE TABLE `trails` (
  `trail_id` int PRIMARY KEY,
  `wikiloc_id` INT,
  `title` TEXT,
  `url` TEXT,
  `user_id` INT,
  `category_id` INT,
  `country` TEXT,
  `distance` FLOAT,
  `loop` BOOL,
  `elevation_gain` FLOAT,
  `elevation_loss` FLOAT,
  `elevation_max` FLOAT,
  `elevation_min` FLOAT,
  `moving_time` INT,
  `total_time` INT,
  `uploaded` TEXT,
  `recorded` TEXT,
  `n_coords` INT,
  `difficulty` INT
);

DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
  `category_id` int PRIMARY KEY,
  `category_name` TEXT
);

CREATE TABLE `users` (
  `user_id` int PRIMARY KEY,
  `wikiloc_user_id` int,
  `user_name` TEXT
);

CREATE INDEX category_id_idx ON `trails` (`category_id`);

CREATE INDEX user_ids_idx ON `users` (user_id, wikiloc_user_id);

ALTER TABLE `categories` ADD FOREIGN KEY (`category_id`) REFERENCES `trails` (`category_id`);

CREATE INDEX user_id_idx ON `trails` (`user_id`);

ALTER TABLE `users` ADD FOREIGN KEY (`user_id`) REFERENCES `trails` (`user_id`);

CREATE INDEX `trail_ids_idx` ON `trails` (`trail_id`, `wikiloc_id`);

USE trails;

SELECT DATABASE();

SHOW TABLES;

DESCRIBE trails;

DESCRIBE users;

DESCRIBE categories;