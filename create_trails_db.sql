DROP DATABASE IF EXISTS `trails`;
CREATE DATABASE `trails`;
USE `trails`;

DROP TABLE IF EXISTS trails;
CREATE TABLE `trails` (
  `trail_id` int PRIMARY KEY AUTO_INCREMENT,
  `wikiloc_id` INT,
  `title` TEXT,
  `url` TEXT,
  `user_id` INT,
  `category_id` INT,
  `country` TEXT,
  `distance` FLOAT,
  `is_loop` BOOL,
  `elevation_gain` FLOAT,
  `elevation_loss` FLOAT,
  `elevation_max` FLOAT,
  `elevation_min` FLOAT,
  `moving_time` INT,
  `total_time` INT,
  `uploaded` TEXT,
  `recorded` TEXT,
  `n_coords` INT,
  `difficulty` INT,
  `near_place` TEXT,
  `near_area` TEXT,
  `near_country` TEXT,
  `start_lat` DOUBLE,
  `start_lon` DOUBLE,
  `photo_urls` TEXT
);

DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
  `category_id` int PRIMARY KEY,
  `category_name` TEXT
);

CREATE TABLE `users` (
  `user_id` int PRIMARY KEY AUTO_INCREMENT,
  `wikiloc_user_id` int,
  `user_name` TEXT
);

CREATE INDEX category_id_idx ON `trails` (`category_id`);

CREATE INDEX user_ids_idx ON `users` (user_id, wikiloc_user_id);

ALTER TABLE `trails` ADD FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`);

CREATE INDEX user_id_idx ON `trails` (`user_id`);

ALTER TABLE `trails` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

CREATE INDEX `trail_ids_idx` ON `trails` (`trail_id`, `wikiloc_id`);

USE trails;

SELECT DATABASE();

SHOW TABLES;

DESCRIBE trails;

DESCRIBE users;

DESCRIBE categories;

INSERT INTO categories(category_id,category_name)
VALUES
    (1,'mountain biking'),
    (2,'hiking'),
    (3,'cycling'),
    (4,'running'),
    (5,'trail running '),
    (6,'mountaineering'),
    (7,'bicycle touring'),
    (8,'walking'),
    (9,'motorcycling'),
    (10,'ack country skiing'),
    (11,'rail bike'),
    (12,'atv'),
    (13,'kayaking - canoeing'),
    (14,'sailing'),
    (15,'snowshoeing'),
    (16,'cross country skiing'),
    (17,'alpine skiing'),
    (18,'flying'),
    (19,'horseback riding'),
    (20,'dog sledging'),
    (21,'rock climbing'),
    (22,'inline skating'),
    (23,'skating'),
    (24,'train'),
    (25,'canyoneering'),
    (26,'diving'),
    (27,'caving'),
    (28,'hang gliding'),
    (29,'ballooning'),
    (30,'snowboarding'),
    (31,'ice climbing'),
    (32,'snowmobiling'),
    (33,'accessible'),
    (34,'offroading'),
    (35,'rowing'),
    (36,'car'),
    (37,'kiteboarding'),
    (38,'kite skiing'),
    (39,'sledge'),
    (40,'kickbike'),
    (41,'paragliding'),
    (42,'for blind'),
    (43,'nordic walking'),
    (44,'motorcycle trials'),
    (45,'enduro'),
    (46,'via ferrata'),
    (47,'swimming'),
    (48,'orienteering'),
    (49,'multisport'),
    (50,'stand up paddle (sup)'),
    (51,'barefoot'),
    (52,'canicross'),
    (53,'roller skiing'),
    (54,'longboarding'),
    (55,'mountain unicycling'),
    (56,'golf'),
    (57,'recreational vehicle'),
    (58,'airboat'),
    (59,'segway'),
    (60,'camel'),
    (61,'freeride'),
    (62,'unmanned aerial vehicle (uav)'),
    (63,'motorboat'),
    (64,'birdwatching - birding'),
    (65,'trailer bike'),
    (66,'water scooter (pwc)'),
    (67,'handbike'),
    (68,'rafting'),
    (69,'downhill mountain biking (dh)'),
    (70,'ebike'),
    (71,'base jumping'),
    (72,'joëlette'),
    (73,'with baby carriage'),
    (74,'splitboard'),
    (75,'gravel bike');

