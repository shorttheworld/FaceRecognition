-- phpMyAdmin SQL Dump
-- version 4.0.4
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Nov 24, 2013 at 09:38 PM
-- Server version: 5.6.12-log
-- PHP Version: 5.4.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `inyoface`
--
CREATE DATABASE IF NOT EXISTS `inyoface` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `inyoface`;

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE IF NOT EXISTS `admin` (
  `USERNAME` varchar(65) NOT NULL,
  `PASS_HASH` varchar(8192) NOT NULL,
  PRIMARY KEY (`USERNAME`),
  UNIQUE KEY `USERNAME` (`USERNAME`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`USERNAME`, `PASS_HASH`) VALUES
('scollestan', 'asdf');

-- --------------------------------------------------------

--
-- Table structure for table `learner`
--

CREATE TABLE IF NOT EXISTS `learner` (
  `LEARNER` longblob NOT NULL,
  `TIME_STAMP` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`TIME_STAMP`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `FIRST_NAME` varchar(20) NOT NULL,
  `LAST_NAME` varchar(65) NOT NULL,
  `USERNAME` varchar(65) NOT NULL,
  PRIMARY KEY (`USERNAME`),
  UNIQUE KEY `USERNAME_2` (`USERNAME`),
  KEY `USERNAME` (`USERNAME`),
  KEY `USERNAME_3` (`USERNAME`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`FIRST_NAME`, `LAST_NAME`, `USERNAME`) VALUES
('Chris', 'Adams', '1234'),
('asdffgh', 'asdfdfgh', 'asdfaswahd'),
('TEST', 'ME', 'FYCGUIUYIYVBI'),
('THIS', 'IS', 'GARCON'),
('o0ikpjmln', 'jiopmnklm', 'iojkm lk'),
('fcgvbhvujh', 'kjvuyvguyjhvg', 'ivhubiub'),
('iopjkionjk', 'jiokjionk', 'joinjiounk'),
('Solace', 'Collestan', 'scollestan'),
('sadfasfdfg', 'sfgsdfghjhg', 'sdgfhfdsag'),
('TEST', 'USER', 'tfrcyvukytychg'),
('qwjuyixdfgrt', 'ezsfjk', 'zefrdk');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
