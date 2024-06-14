-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jun 14, 2024 at 09:04 PM
-- Server version: 8.0.31
-- PHP Version: 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `taloudentasapaino`
--
CREATE DATABASE IF NOT EXISTS `taloudentasapaino` DEFAULT CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci;
USE `taloudentasapaino`;

-- --------------------------------------------------------

--
-- Table structure for table `expenses`
--

DROP TABLE IF EXISTS `expenses`;
CREATE TABLE IF NOT EXISTS `expenses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `amount` int NOT NULL,
  `transaction_dt` datetime NOT NULL,
  `expense_classifications_id` int NOT NULL,
  `users_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_expenses_expense_classifications_idx` (`expense_classifications_id`),
  KEY `fk_expenses_users1_idx` (`users_id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `expenses`
--

INSERT INTO `expenses` (`id`, `amount`, `transaction_dt`, `expense_classifications_id`, `users_id`) VALUES
(13, 10, '2024-06-05 16:17:15', 1, NULL),
(14, 20, '2024-06-05 16:27:36', 1, NULL),
(20, 99, '2024-06-14 23:03:06', 1, NULL),
(21, 80, '2024-06-14 23:08:39', 1, NULL),
(22, 4100, '2024-06-14 23:09:13', 20, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `expense_classifications`
--

DROP TABLE IF EXISTS `expense_classifications`;
CREATE TABLE IF NOT EXISTS `expense_classifications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `expense_type` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `expense_classifications`
--

INSERT INTO `expense_classifications` (`id`, `name`, `expense_type`) VALUES
(1, 'Ruoka', 'withdrawal'),
(20, 'Palkka', 'income'),
(22, 'Koti', 'withdrawal');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `password` varchar(255) NOT NULL,
  `access_jti` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `access_jti`) VALUES
(1, 'juhani', '$pbkdf2-sha512$25000$9N7bOyckBGDsPQeA8H4vRQ$8yOSWGFSltzy1IX7g7hJEP1Ah.8Mlpu283p64vOooPgJ0s/VtLKpNEglrvrUwu8QX/I2.xTObbu53s66TQ5JVw', '0f2e9b5c-7f6a-4b46-bf53-ca65f4f83392');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `expenses`
--
ALTER TABLE `expenses`
  ADD CONSTRAINT `fk_expenses_expense_classifications` FOREIGN KEY (`expense_classifications_id`) REFERENCES `expense_classifications` (`id`),
  ADD CONSTRAINT `fk_expenses_users1` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
