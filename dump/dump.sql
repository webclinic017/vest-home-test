CREATE DATABASE `vest` /*!40100 COLLATE 'utf8mb4_0900_ai_ci' */;
USE `vest`;

CREATE TABLE `shares` (
	`amount` FLOAT NULL DEFAULT NULL
)
COLLATE='utf8mb4_0900_ai_ci'
;

CREATE TABLE `orders` (
	`action` CHAR(50) NULL DEFAULT NULL,
	`symbol` CHAR(50) NULL DEFAULT NULL,
	`price` CHAR(50) NULL DEFAULT NULL,
	`shares` CHAR(50) NULL DEFAULT NULL,
	`datetime` DATETIME NULL DEFAULT NULL
);
COLLATE='utf8mb4_0900_ai_ci'
;


