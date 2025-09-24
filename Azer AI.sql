-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Anamakine: 127.0.0.1:3306
-- Üretim Zamanı: 18 Nis 2025, 20:25:59
-- Sunucu sürümü: 9.1.0
-- PHP Sürümü: 8.3.14

SET FOREIGN_KEY_CHECKS = 0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- Veritabanı: `azerai`

-- --------------------------------------------------------

DROP TABLE IF EXISTS `custom_commands`;
CREATE TABLE `custom_commands` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `action` varchar(100) NOT NULL,
  `target` text NOT NULL,
  `triggers_az` text NOT NULL,
  `triggers_tr` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

INSERT INTO `custom_commands` VALUES
(1, 1, 'google ac', 'Program Aç', 'C:/Program Files/Google/Chrome/Application/chrome.exe', 'google aç', 'google', '2025-04-04 22:57:10');

-- --------------------------------------------------------

DROP TABLE IF EXISTS `pro_keys`;
CREATE TABLE `pro_keys` (
  `id` int NOT NULL AUTO_INCREMENT,
  `key_code` varchar(50) NOT NULL,
  `duration` int NOT NULL DEFAULT 30,
  `status` varchar(20) NOT NULL DEFAULT 'unused',
  `activation_date` datetime DEFAULT NULL,
  `used_by` int DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_code` (`key_code`),
  KEY `used_by` (`used_by`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

INSERT INTO `pro_keys` VALUES
(1, 'PRO234-567-830', 30, 'unused', NULL, NULL, '2025-04-04 22:57:10'),
(2, 'PRO234-567-890', 90, 'unused', NULL, NULL, '2025-04-04 22:57:10'),
(3, 'PRO345-678-180', 180, 'unused', NULL, NULL, '2025-04-04 22:57:10');

-- --------------------------------------------------------

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `role` varchar(20) NOT NULL DEFAULT 'user',
  `license_status` varchar(20) NOT NULL DEFAULT 'free',
  `last_login` datetime DEFAULT NULL,
  `pro_expiry` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

INSERT INTO `users` VALUES
(1, 'admin', '$2y$10$DLUGxUMpE5g00b74kwVtdOWDmxSCPkBMyhmbeuhN8R4g/BGsmSQeW', 'Admin User', 'admin', 'pro', '2025-03-31 00:24:04', NULL, '2025-04-04 22:57:10');

-- --------------------------------------------------------

DROP TABLE IF EXISTS `version`;
CREATE TABLE `version` (
  `id` int NOT NULL AUTO_INCREMENT,
  `version` varchar(10) NOT NULL,
  `web_url` varchar(255) DEFAULT NULL,
  `info` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

INSERT INTO `version` VALUES
(1, 'V1.0', 'https://github.com/QadirAbbasov/Azer-AI', 'Yeni versiyada aşağıdakı yeniliklər var:\n- Performans yaxşılaşdırmaları\n- Yeni xüsusiyyətlər\n- Xətaların düzəldilməsi', '2025-04-19 00:25:39');

-- --------------------------------------------------------

DROP TABLE IF EXISTS `voice_settings`;
CREATE TABLE `voice_settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `tts_engine` varchar(20) DEFAULT 'edge',
  `language` varchar(20) DEFAULT 'az-AZ',
  `voice_gender` varchar(20) DEFAULT 'male',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

INSERT INTO `voice_settings` VALUES
(1, 1, 'edge', 'az-AZ', 'male');

-- --------------------------------------------------------

DROP TABLE IF EXISTS `wake_word_settings`;
CREATE TABLE `wake_word_settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `az_word` varchar(50) DEFAULT 'azər',
  `tr_word` varchar(50) DEFAULT 'azer',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

INSERT INTO `wake_word_settings` VALUES
(1, 1, 'azər', 'azer');

-- --------------------------------------------------------

-- FOREIGN KEY KISITLAMALARI EN SONDA EKLENİYOR
ALTER TABLE `custom_commands`
  ADD CONSTRAINT `custom_commands_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

ALTER TABLE `pro_keys`
  ADD CONSTRAINT `pro_keys_ibfk_1` FOREIGN KEY (`used_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;

ALTER TABLE `voice_settings`
  ADD CONSTRAINT `voice_settings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

ALTER TABLE `wake_word_settings`
  ADD CONSTRAINT `wake_word_settings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;


COMMIT;
SET FOREIGN_KEY_CHECKS = 1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
