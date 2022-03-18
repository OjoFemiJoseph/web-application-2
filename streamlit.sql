
--
-- Database: `upwork`
--

-- --------------------------------------------------------

--
-- Table structure for table `streamlit`
--


CREATE TABLE `streamlith` (
  `id`    INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `title` varchar(255) NOT NULL,
  `col_a` varchar(255) NOT NULL,
  `col_b` varchar(255) NOT NULL,
  `file_location` varchar(255) NOT NULL,
  `file_type` varchar(50) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
