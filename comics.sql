-- phpMyAdmin SQL Dump
-- version 4.7.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Oct 23, 2017 at 12:25 AM
-- Server version: 5.6.35
-- PHP Version: 7.0.22

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `comics`
--

-- --------------------------------------------------------

--
-- Table structure for table `comic`
--

CREATE TABLE `comic` (
  `id` int(11) NOT NULL,
  `title` varchar(120) NOT NULL,
  `issue_number` int(11) NOT NULL,
  `year` varchar(4) NOT NULL,
  `publisher_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `comic`
--

INSERT INTO `comic` (`id`, `title`, `issue_number`, `year`, `publisher_id`) VALUES
(4, 'The Amazing Spider-man', 1, '1963', 1),
(9, 'The Amazing Spider-man', 2, '1963', 1),
(10, 'The Amazing Spider-man', 3, '1963', 1),
(11, 'The Amazing Spider-man', 4, '1963', 1),
(12, 'The Amazing Spider-man', 5, '1963', 1),
(13, 'Batman', 1, '1940', 2),
(14, 'Batman', 2, '1940', 2),
(15, 'Batman', 3, '1940', 2),
(16, 'Batman', 4, '1940', 2),
(17, 'Wonder Woman', 1, '1942', 2),
(18, 'Wonder Woman', 2, '1942', 2),
(19, 'Wonder Woman', 3, '1942', 2),
(20, 'Wonder Woman', 4, '1942', 2),
(21, 'Wolverine', 1, '1982', 1),
(22, 'X-Men', 1, '1963', 1);

-- --------------------------------------------------------

--
-- Table structure for table `publisher`
--

CREATE TABLE `publisher` (
  `id` int(11) NOT NULL,
  `name` varchar(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `publisher`
--

INSERT INTO `publisher` (`id`, `name`) VALUES
(1, 'Marvel'),
(2, 'DC');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `email`, `password`) VALUES
(1, 'welzie@gmail.com', '1234');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `comic`
--
ALTER TABLE `comic`
  ADD PRIMARY KEY (`id`),
  ADD KEY `publisher_id` (`publisher_id`);

--
-- Indexes for table `publisher`
--
ALTER TABLE `publisher`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `comic`
--
ALTER TABLE `comic`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;
--
-- AUTO_INCREMENT for table `publisher`
--
ALTER TABLE `publisher`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `comic`
--
ALTER TABLE `comic`
  ADD CONSTRAINT `comic_ibfk_1` FOREIGN KEY (`publisher_id`) REFERENCES `publisher` (`id`);
