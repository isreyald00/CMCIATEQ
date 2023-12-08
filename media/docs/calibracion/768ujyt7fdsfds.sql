-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 30, 2023 at 10:56 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cmciateq`
--

-- --------------------------------------------------------

--
-- Table structure for table `metrologia_detallecontrolmetro`
--

CREATE TABLE `metrologia_detallecontrolmetro` (
  `id` bigint(20) NOT NULL,
  `valor_esperado` varchar(100) NOT NULL,
  `id_controlMetro_id` varchar(20) NOT NULL,
  `id_criterio_id` varchar(20) NOT NULL,
  `id_unidad_criterio_id` varchar(10) NOT NULL,
  `rango` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `metrologia_detallecontrolmetro`
--

INSERT INTO `metrologia_detallecontrolmetro` (`id`, `valor_esperado`, `id_controlMetro_id`, `id_criterio_id`, `id_unidad_criterio_id`, `rango`) VALUES
(141, '5', 'LS-E-0001-M-HI', 'Error', '%', 'Max'),
(142, '556', 'IP-A-0001-A-JL', 'Error', '%', 'Max'),
(143, '4', 'IP-A-0001-A-JL', 'Incertidumbre', '%', 'Max'),
(144, '55', 'LS-E-0001-M-HI', 'Incertidumbre', '%', 'Max'),
(145, '3', 'SM-G-0001-I-SL', 'Error', 'L/min', 'Max'),
(146, '4', 'SM-G-0001-I-SL', 'Incertidumbre', 'lbf·ft', 'Max'),
(147, '5', 'SM-G-0002-I-SL', 'Error', '%', 'Max'),
(148, '899', 'SM-G-0002-I-SL', 'Incertidumbre', '%', 'Max'),
(149, '556', 'SM-G-0003-I-SL', 'Error', '%', 'Max'),
(150, '899', 'SM-G-0003-I-SL', 'Incertidumbre', '%', 'Max'),
(151, '3', 'IV-T-0002-I-TA', 'Error', 'L', 'Max'),
(152, '4', 'IV-T-0002-I-TA', 'Incertidumbre', 'lbf', 'Max'),
(153, '556', 'PM-I-0004-A-AS', 'Error', 'lbf', 'Max'),
(154, '1', 'PM-G-0002-A-TA', 'Error', '%', 'Max'),
(155, '4', 'PM-G-0002-A-TA', 'Incertidumbre', '%', 'Max'),
(156, '1', 'IV-T-0001-I-TA', 'Error', '%', 'Max'),
(157, '1', 'PM-H-0001-A-EM', 'Error', '%', 'Max'),
(158, 'd', 'PM-H-0002-A-EM', 'Error', '%', 'Max'),
(159, '556', 'PM-H-0003-A-EM', 'Error', '%', 'Max'),
(160, '4', 'PM-H-0003-A-EM', 'Incertidumbre', '%', 'Max'),
(161, '556', 'PM-H-0004-A-EM', 'Error', '%', 'Max'),
(162, '5', 'PM-H-0005-A-EM', 'Error', 'kgf', 'Max'),
(163, '899', 'PM-H-0005-A-EM', 'Incertidumbre', 'kgf·m', 'Max'),
(164, '556', 'PM-H-0006-A-EM', 'Error', 'C', 'Max'),
(165, '4', 'PM-H-0006-A-EM', 'Incertidumbre', 'bar', 'Max'),
(166, '1', 'PM-H-0007-A-EM', 'Error', '%', 'Max'),
(167, '4', 'PM-H-0007-A-EM', 'Incertidumbre', '%', 'Max'),
(168, '556', 'PM-H-0001-P-TA', 'Error', '%', 'Max'),
(169, '899', 'PM-H-0001-P-TA', 'Incertidumbre', '%', 'Max'),
(170, '5', 'PM-H-0002-P-TA', 'Error', '%', 'Max'),
(171, '899', 'PM-H-0002-P-TA', 'Incertidumbre', '%', 'Max'),
(172, '556', 'PM-H-0003-P-TA', 'Error', '%', 'Max'),
(173, '4', 'PM-H-0003-P-TA', 'Incertidumbre', '%', 'Max'),
(174, '556', 'PM-H-0004-P-TA', 'Error', '%', 'Max'),
(175, '4', 'PM-H-0004-P-TA', 'Incertidumbre', '%', 'Max'),
(176, '1', 'PM-H-0005-P-TA', 'Error', '%', 'Max'),
(177, '899', 'PM-H-0005-P-TA', 'Incertidumbre', '%', 'Max'),
(178, '556', 'PM-H-0006-P-TA', 'Error', '%', 'Max'),
(179, '899', 'PM-H-0006-P-TA', 'Incertidumbre', '%', 'Max'),
(180, '55', 'PM-H-0007-P-TA', 'Error', '%', 'Max'),
(181, '4', 'PM-H-0007-P-TA', 'Incertidumbre', '%', 'Max'),
(182, '1', 'PM-H-0008-P-TA', 'Error', '%', 'Max'),
(183, '4', 'PM-H-0008-P-TA', 'Incertidumbre', '%', 'Max'),
(184, '556', 'PM-H-0009-P-TA', 'Error', '%', 'Max'),
(185, '4', 'PM-H-0009-P-TA', 'Incertidumbre', '%', 'Max'),
(186, '1', 'LS-F-0001-P-JL', 'Error', '%', 'Max'),
(187, '4', 'LS-F-0001-P-JL', 'Incertidumbre', '%', 'Max'),
(188, '556', 'LS-F-0002-P-JL', 'Error', '%', 'Max'),
(189, '899', 'LS-F-0002-P-JL', 'Incertidumbre', '%', 'Max'),
(190, '5', 'LS-F-0003-P-JL', 'Error', '%', 'Max'),
(191, '5', 'LS-F-0003-P-JL', 'Incertidumbre', '%', 'Max'),
(192, '5', 'LS-F-0003-P-JL', 'Linealidad', '%', 'Max'),
(193, '5', 'LS-F-0003-P-JL', 'Repetibilidad', '%', 'Max'),
(194, '1', 'LS-F-0004-P-JL', 'Error', '%', 'Max'),
(195, '4', 'LS-F-0004-P-JL', 'Incertidumbre', '%', 'Max'),
(198, '5', 'LS-F-0004-P-JL', 'Error', '%', 'Max'),
(199, '4', 'LS-F-0004-P-JL', 'Incertidumbre', '%', 'Max'),
(200, '5', 'LS-F-0004-P-JL', 'Error', '%', 'Max'),
(222, '1', 'LS-F-0004-P-JL', 'Error', '%', 'Max'),
(223, '4', 'LS-F-0004-P-JL', 'Incertidumbre', '%', 'Max'),
(224, '1', 'LS-F-0004-P-JL', 'Error', '%', 'Max'),
(225, '4', 'LS-F-0004-P-JL', 'Incertidumbre', '%', 'Max'),
(226, '1', 'LS-F-0004-P-JL', 'Error', '%', 'Max'),
(227, '4', 'LS-F-0004-P-JL', 'Incertidumbre', '%', 'Max'),
(228, '1', 'LS-F-0004-P-JL', 'Error', '%', 'Max'),
(229, '4', 'LS-F-0004-P-JL', 'Incertidumbre', '%', 'Max'),
(230, '1', 'LS-F-0004-P-JL', 'Error', '%', 'Max'),
(231, '4', 'LS-F-0004-P-JL', 'Incertidumbre', '%', 'Max'),
(232, '1', 'LS-F-0004-P-JL', 'Error', '%', 'Max'),
(233, '4', 'LS-F-0004-P-JL', 'Incertidumbre', '%', 'Max'),
(234, '1', 'LS-F-0004-P-JL', 'Error', '%', 'Max'),
(235, '4', 'LS-F-0004-P-JL', 'Incertidumbre', '%', 'Max'),
(238, '1', 'LS-F-0004-P-JL', 'Error', '%', 'Max'),
(239, '4', 'LS-F-0004-P-JL', 'Incertidumbre', '%', 'Max'),
(240, '1', 'LS-F-0004-P-JL', 'Error', '%', 'Max'),
(241, '4', 'LS-F-0004-P-JL', 'Incertidumbre', '%', 'Max'),
(242, '556', 'LS-F-0004-P-JL', 'Error', '%', 'Max'),
(243, '4', 'LS-F-0004-P-JL', 'Incertidumbre', '%', 'Max'),
(244, '1', 'LS-F-0004-P-JL', 'Error', '%', 'Max'),
(245, '4', 'LS-F-0004-P-JL', 'Incertidumbre', '%', 'Max'),
(246, '1', 'LS-F-0004-P-JL', 'Error', '%', 'Max'),
(247, '4', 'LS-F-0004-P-JL', 'Incertidumbre', '%', 'Max'),
(248, '1', 'LS-F-0004-P-JL', 'Error', '%', 'Max'),
(249, '4', 'LS-F-0004-P-JL', 'Incertidumbre', '%', 'Max'),
(250, '556', 'LS-F-0004-P-JL', 'Error', '%', 'Max'),
(251, '4', 'LS-F-0004-P-JL', 'Incertidumbre', '%', 'Max'),
(252, '556', 'LS-F-0004-P-JL', 'Error', '%', 'Max'),
(253, '4', 'LS-F-0004-P-JL', 'Incertidumbre', '%', 'Max'),
(254, '556', 'LS-F-0004-P-JL', 'Error', '%', 'Max'),
(255, '4', 'LS-F-0004-P-JL', 'Incertidumbre', '%', 'Max');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `metrologia_detallecontrolmetro`
--
ALTER TABLE `metrologia_detallecontrolmetro`
  ADD PRIMARY KEY (`id`),
  ADD KEY `metrologia_detalleco_id_controlMetro_id_907d2a58_fk_metrologi` (`id_controlMetro_id`),
  ADD KEY `metrologia_detalleco_id_unidad_criterio_i_706961af_fk_metrologi` (`id_unidad_criterio_id`),
  ADD KEY `metrologia_detallecontrolmetro_id_criterio_id_e58bfe5b` (`id_criterio_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `metrologia_detallecontrolmetro`
--
ALTER TABLE `metrologia_detallecontrolmetro`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=256;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `metrologia_detallecontrolmetro`
--
ALTER TABLE `metrologia_detallecontrolmetro`
  ADD CONSTRAINT `metrologia_detalleco_id_controlMetro_id_907d2a58_fk_metrologi` FOREIGN KEY (`id_controlMetro_id`) REFERENCES `metrologia_controlmetro` (`id_equipo_id`),
  ADD CONSTRAINT `metrologia_detalleco_id_unidad_criterio_i_706961af_fk_metrologi` FOREIGN KEY (`id_unidad_criterio_id`) REFERENCES `metrologia_unidad` (`id`),
  ADD CONSTRAINT `metrologia_detallecontrolmetro_id_criterio_id_e58bfe5b_fk` FOREIGN KEY (`id_criterio_id`) REFERENCES `metrologia_criterio` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
