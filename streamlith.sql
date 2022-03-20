DROP DATABASE IF EXISTS `upwork`;
CREATE DATABASE `upwork`;
--
-- Database: `upwork`
--

-- --------------------------------------------------------

--
-- Table structure for table `streamlith`
--

CREATE TABLE `streamlith` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `col_a` varchar(255) NOT NULL,
  `col_b` varchar(255) NOT NULL,
  `file_location` varchar(255) NOT NULL,
  `file_type` varchar(50) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `update_column` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for table `streamlith`
--
ALTER TABLE `streamlith`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `streamlith`
--
ALTER TABLE `streamlith`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
