CREATE DATABASE `vest` /*!40100 COLLATE 'utf8mb4_0900_ai_ci' */;
USE `vest`;

CREATE TABLE `shares` (
	`symbol` CHAR(50) NULL DEFAULT NULL,
	`shares` FLOAT NULL DEFAULT NULL
)
COLLATE='utf8mb4_0900_ai_ci'
;

CREATE TABLE `orders` (
	`action` CHAR(50) NULL DEFAULT NULL,
	`symbol` CHAR(50) NULL DEFAULT NULL,
	`price` FLOAT NULL DEFAULT NULL,
	`shares` FLOAT NULL DEFAULT NULL,
	`datetime` DATETIME NULL DEFAULT NULL
);
COLLATE='utf8mb4_0900_ai_ci'
;


