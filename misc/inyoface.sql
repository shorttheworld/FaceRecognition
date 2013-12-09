-- phpMyAdmin SQL Dump
-- version 4.0.4
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Dec 09, 2013 at 04:25 AM
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
  `USERNAME` varchar(15) NOT NULL,
  `PASS_HASH` varchar(255) NOT NULL,
  UNIQUE KEY `USERNAME` (`USERNAME`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`USERNAME`, `PASS_HASH`) VALUES
('admin', 'aeb37d91ec0137985476736428db4ba3675c47587df0d63318afc82335cc989fa9c065d2b97209b2d273bb09ad90812847203b432ef9d6dc3319545517b77380'),
('Garcon', '5c901b0c73460cbd06429bd825c8fff85d0b7ba65fd05213aed188a071a072cd9a395a877cacdff2da3503eef092b0fac7b2982bd43d12c7498042a16c27bc42'),
('Hannah', '6e5851a3b5c72e49f5a3ed405c1d93ad16b6b542846430e06037bbe8d47dab70a64b88374be2c229cb3152d4885ff822c42c122cd8112bce87b9e55c5da855d8');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `user_index` int(8) NOT NULL AUTO_INCREMENT,
  `username` varchar(500) NOT NULL,
  `first_name` varchar(500) NOT NULL,
  `last_name` varchar(500) NOT NULL,
  `active` int(1) NOT NULL,
  PRIMARY KEY (`user_index`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=107 ;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_index`, `username`, `first_name`, `last_name`, `active`) VALUES
(103, 'testpass', 'Saman', 'Shareghi', 1),
(104, 'Hannah', 'Hannah', 'Lau', 1),
(106, 'Garcon', 'Chris', 'Adams', 1);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
