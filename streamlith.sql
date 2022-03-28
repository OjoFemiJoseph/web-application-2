CREATE DATABASE IF NOT EXISTS upwork;

DROP TABLE IF EXISTS `streamlith`;

CREATE TABLE `streamlith` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `title` varchar(255) ,
  `title2` varchar(255) ,
  `col_a` varchar(255) ,
  `col_b` varchar(255) ,
  `file_location` varchar(255) ,
  `file_type` varchar(50) ,
  `created_at` timestamp  DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `update_column` varchar(100) 
);
