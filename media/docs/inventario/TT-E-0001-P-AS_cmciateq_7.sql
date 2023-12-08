-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 05, 2023 at 03:54 PM
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
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(1, 'Admin'),
(2, 'Capturista'),
(3, 'Solo lectura');

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add custom user', 6, 'add_customuser'),
(22, 'Can change custom user', 6, 'change_customuser'),
(23, 'Can delete custom user', 6, 'delete_customuser'),
(24, 'Can view custom user', 6, 'view_customuser'),
(25, 'Can add baja', 7, 'add_baja'),
(26, 'Can change baja', 7, 'change_baja'),
(27, 'Can delete baja', 7, 'delete_baja'),
(28, 'Can view baja', 7, 'view_baja'),
(29, 'Can add clasificacion', 8, 'add_clasificacion'),
(30, 'Can change clasificacion', 8, 'change_clasificacion'),
(31, 'Can delete clasificacion', 8, 'delete_clasificacion'),
(32, 'Can view clasificacion', 8, 'view_clasificacion'),
(33, 'Can add direccion especialidad', 9, 'add_direccionespecialidad'),
(34, 'Can change direccion especialidad', 9, 'change_direccionespecialidad'),
(35, 'Can delete direccion especialidad', 9, 'delete_direccionespecialidad'),
(36, 'Can view direccion especialidad', 9, 'view_direccionespecialidad'),
(37, 'Can add docs', 10, 'add_docs'),
(38, 'Can change docs', 10, 'change_docs'),
(39, 'Can delete docs', 10, 'delete_docs'),
(40, 'Can view docs', 10, 'view_docs'),
(41, 'Can add magnitud', 11, 'add_magnitud'),
(42, 'Can change magnitud', 11, 'change_magnitud'),
(43, 'Can delete magnitud', 11, 'delete_magnitud'),
(44, 'Can view magnitud', 11, 'view_magnitud'),
(45, 'Can add sede', 12, 'add_sede'),
(46, 'Can change sede', 12, 'change_sede'),
(47, 'Can delete sede', 12, 'delete_sede'),
(48, 'Can view sede', 12, 'view_sede'),
(49, 'Can add tipo doc', 13, 'add_tipodoc'),
(50, 'Can change tipo doc', 13, 'change_tipodoc'),
(51, 'Can delete tipo doc', 13, 'delete_tipodoc'),
(52, 'Can view tipo doc', 13, 'view_tipodoc'),
(53, 'Can add equipo', 14, 'add_equipo'),
(54, 'Can change equipo', 14, 'change_equipo'),
(55, 'Can delete equipo', 14, 'delete_equipo'),
(56, 'Can view equipo', 14, 'view_equipo'),
(57, 'Can add criterio', 15, 'add_criterio'),
(58, 'Can change criterio', 15, 'change_criterio'),
(59, 'Can delete criterio', 15, 'delete_criterio'),
(60, 'Can view criterio', 15, 'view_criterio'),
(61, 'Can add unidad', 16, 'add_unidad'),
(62, 'Can change unidad', 16, 'change_unidad'),
(63, 'Can delete unidad', 16, 'delete_unidad'),
(64, 'Can view unidad', 16, 'view_unidad'),
(65, 'Can add especificacion metrologia', 17, 'add_especificacionmetrologia'),
(66, 'Can change especificacion metrologia', 17, 'change_especificacionmetrologia'),
(67, 'Can delete especificacion metrologia', 17, 'delete_especificacionmetrologia'),
(68, 'Can view especificacion metrologia', 17, 'view_especificacionmetrologia'),
(69, 'Can add criterios metrologicos', 18, 'add_criteriosmetrologicos'),
(70, 'Can change criterios metrologicos', 18, 'change_criteriosmetrologicos'),
(71, 'Can delete criterios metrologicos', 18, 'delete_criteriosmetrologicos'),
(72, 'Can view criterios metrologicos', 18, 'view_criteriosmetrologicos'),
(73, 'Can add calibracion', 19, 'add_calibracion'),
(74, 'Can change calibracion', 19, 'change_calibracion'),
(75, 'Can delete calibracion', 19, 'delete_calibracion'),
(76, 'Can view calibracion', 19, 'view_calibracion'),
(77, 'Can add criterios calibracion', 20, 'add_criterioscalibracion'),
(78, 'Can change criterios calibracion', 20, 'change_criterioscalibracion'),
(79, 'Can delete criterios calibracion', 20, 'delete_criterioscalibracion'),
(80, 'Can view criterios calibracion', 20, 'view_criterioscalibracion'),
(81, 'Can add especificacion calibracion', 21, 'add_especificacioncalibracion'),
(82, 'Can change especificacion calibracion', 21, 'change_especificacioncalibracion'),
(83, 'Can delete especificacion calibracion', 21, 'delete_especificacioncalibracion'),
(84, 'Can view especificacion calibracion', 21, 'view_especificacioncalibracion'),
(85, 'Can add especificacion verificacion', 22, 'add_especificacionverificacion'),
(86, 'Can change especificacion verificacion', 22, 'change_especificacionverificacion'),
(87, 'Can delete especificacion verificacion', 22, 'delete_especificacionverificacion'),
(88, 'Can view especificacion verificacion', 22, 'view_especificacionverificacion'),
(89, 'Can add verificacion', 23, 'add_verificacion'),
(90, 'Can change verificacion', 23, 'change_verificacion'),
(91, 'Can delete verificacion', 23, 'delete_verificacion'),
(92, 'Can view verificacion', 23, 'view_verificacion'),
(93, 'Can add detalle mantenimiento externo', 24, 'add_detallemantenimientoexterno'),
(94, 'Can change detalle mantenimiento externo', 24, 'change_detallemantenimientoexterno'),
(95, 'Can delete detalle mantenimiento externo', 24, 'delete_detallemantenimientoexterno'),
(96, 'Can view detalle mantenimiento externo', 24, 'view_detallemantenimientoexterno'),
(97, 'Can add especificacion mantenimiento', 25, 'add_especificacionmantenimiento'),
(98, 'Can change especificacion mantenimiento', 25, 'change_especificacionmantenimiento'),
(99, 'Can delete especificacion mantenimiento', 25, 'delete_especificacionmantenimiento'),
(100, 'Can view especificacion mantenimiento', 25, 'view_especificacionmantenimiento'),
(101, 'Can add detalle mantenimiento interno', 26, 'add_detallemantenimientointerno'),
(102, 'Can change detalle mantenimiento interno', 26, 'change_detallemantenimientointerno'),
(103, 'Can delete detalle mantenimiento interno', 26, 'delete_detallemantenimientointerno'),
(104, 'Can view detalle mantenimiento interno', 26, 'view_detallemantenimientointerno'),
(105, 'Can add detalle docs', 27, 'add_detalledocs'),
(106, 'Can change detalle docs', 27, 'change_detalledocs'),
(107, 'Can delete detalle docs', 27, 'delete_detalledocs'),
(108, 'Can view detalle docs', 27, 'view_detalledocs');

-- --------------------------------------------------------

--
-- Table structure for table `calibracion_calibracion`
--

CREATE TABLE `calibracion_calibracion` (
  `cod_cer_cal` varchar(25) NOT NULL,
  `fecha` date NOT NULL,
  `fecha_cap` date NOT NULL,
  `proveedor` varchar(50) NOT NULL,
  `id_patron` varchar(100) NOT NULL,
  `doc` varchar(100) NOT NULL,
  `dictamen` varchar(11) NOT NULL,
  `id_especificacion_id` varchar(20) NOT NULL,
  `resp_cap_id` varchar(254) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `calibracion_calibracion`
--

INSERT INTO `calibracion_calibracion` (`cod_cer_cal`, `fecha`, `fecha_cap`, `proveedor`, `id_patron`, `doc`, `dictamen`, `id_especificacion_id`, `resp_cap_id`) VALUES
('768ujyt7', '2023-11-26', '2023-12-04', 'CIATEQ', 'hghghgfhgfdhgfd', '768ujyt7.html', 'Conforme', 'LS-D-0001-I-JL', 'practicas1.hidalgo@ciateq.mx'),
('768ujyt754', '2023-11-28', '2023-12-04', 'CIATEQ', 'hghghgfhgfdhgfd', '768ujyt754.html', 'Conforme', 'LS-D-0002-I-JL', 'practicas2.hidalgo@ciateq.mx'),
('768ujyt7FGJHGG', '2023-11-27', '2023-12-04', 'CIATEQ', 'hghghgfhgfdhgfd', '768ujyt7FGJHGG.html', 'Conforme', 'LS-D-0001-I-JL', 'practicas1.hidalgo@ciateq.mx');

-- --------------------------------------------------------

--
-- Table structure for table `calibracion_criterioscalibracion`
--

CREATE TABLE `calibracion_criterioscalibracion` (
  `id` bigint(20) NOT NULL,
  `valor` double NOT NULL,
  `cod_cer_cal_id` varchar(25) NOT NULL,
  `id_criterio_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `calibracion_criterioscalibracion`
--

INSERT INTO `calibracion_criterioscalibracion` (`id`, `valor`, `cod_cer_cal_id`, `id_criterio_id`) VALUES
(47, 1, '768ujyt7', 68),
(48, 899, '768ujyt7', 69),
(49, 5, '768ujyt7', 70),
(50, 5, '768ujyt7', 71),
(51, 1, '768ujyt754', 72),
(52, 852, '768ujyt754', 73),
(53, 1, '768ujyt7FGJHGG', 68),
(54, 900, '768ujyt7FGJHGG', 69),
(55, 5, '768ujyt7FGJHGG', 70),
(56, 5, '768ujyt7FGJHGG', 71);

-- --------------------------------------------------------

--
-- Table structure for table `calibracion_especificacioncalibracion`
--

CREATE TABLE `calibracion_especificacioncalibracion` (
  `id_equipo_id` varchar(20) NOT NULL,
  `periodo` int(11) NOT NULL,
  `ultima` date DEFAULT NULL,
  `proxima` date DEFAULT NULL,
  `estatus` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `calibracion_especificacioncalibracion`
--

INSERT INTO `calibracion_especificacioncalibracion` (`id_equipo_id`, `periodo`, `ultima`, `proxima`, `estatus`) VALUES
('IP-D-0001-I-AS', 3, NULL, NULL, 'Pendiente'),
('LS-D-0001-I-JL', 3, '2023-11-27', '2024-02-25', 'Pendiente'),
('LS-D-0002-I-JL', 2, '2023-11-28', '2024-01-27', 'Pendiente'),
('MD-E-0001-I-JL', 3, '2023-12-03', '2024-03-02', 'Pendiente');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` varchar(254) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2023-11-30 22:03:10.409774', '1', 'Admin', 1, '[{\"added\": {}}]', 3, 'practicas1.hidalgo@ciateq.mx'),
(2, '2023-11-30 22:03:31.940942', 'practicas1.hidalgo@ciateq.mx', 'practicas1.hidalgo@ciateq.mx', 2, '[{\"changed\": {\"fields\": [\"Groups\", \"User permissions\", \"Nombre\", \"Apellido p\", \"Apellido m\"]}}]', 6, 'practicas1.hidalgo@ciateq.mx'),
(3, '2023-11-30 22:03:54.871008', '2', 'Capturista', 1, '[{\"added\": {}}]', 3, 'practicas1.hidalgo@ciateq.mx'),
(4, '2023-11-30 22:04:01.771982', '3', 'Solo lectura', 1, '[{\"added\": {}}]', 3, 'practicas1.hidalgo@ciateq.mx');

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(19, 'calibracion', 'calibracion'),
(20, 'calibracion', 'criterioscalibracion'),
(21, 'calibracion', 'especificacioncalibracion'),
(4, 'contenttypes', 'contenttype'),
(7, 'inventario', 'baja'),
(8, 'inventario', 'clasificacion'),
(27, 'inventario', 'detalledocs'),
(9, 'inventario', 'direccionespecialidad'),
(10, 'inventario', 'docs'),
(14, 'inventario', 'equipo'),
(11, 'inventario', 'magnitud'),
(12, 'inventario', 'sede'),
(13, 'inventario', 'tipodoc'),
(24, 'mantenimiento', 'detallemantenimientoexterno'),
(26, 'mantenimiento', 'detallemantenimientointerno'),
(25, 'mantenimiento', 'especificacionmantenimiento'),
(15, 'metrologia', 'criterio'),
(18, 'metrologia', 'criteriosmetrologicos'),
(17, 'metrologia', 'especificacionmetrologia'),
(16, 'metrologia', 'unidad'),
(5, 'sessions', 'session'),
(6, 'usuarios', 'customuser'),
(22, 'verificacion', 'especificacionverificacion'),
(23, 'verificacion', 'verificacion');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2023-11-30 21:57:41.360981'),
(2, 'contenttypes', '0002_remove_content_type_name', '2023-11-30 21:57:41.445598'),
(3, 'auth', '0001_initial', '2023-11-30 21:57:41.777518'),
(4, 'auth', '0002_alter_permission_name_max_length', '2023-11-30 21:57:41.862152'),
(5, 'auth', '0003_alter_user_email_max_length', '2023-11-30 21:57:41.862152'),
(6, 'auth', '0004_alter_user_username_opts', '2023-11-30 21:57:41.877810'),
(7, 'auth', '0005_alter_user_last_login_null', '2023-11-30 21:57:41.893378'),
(8, 'auth', '0006_require_contenttypes_0002', '2023-11-30 21:57:41.893378'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2023-11-30 21:57:41.909000'),
(10, 'auth', '0008_alter_user_username_max_length', '2023-11-30 21:57:41.909000'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2023-11-30 21:57:41.909000'),
(12, 'auth', '0010_alter_group_name_max_length', '2023-11-30 21:57:41.940261'),
(13, 'auth', '0011_update_proxy_permissions', '2023-11-30 21:57:41.946768'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2023-11-30 21:57:41.946768'),
(15, 'usuarios', '0001_initial', '2023-11-30 21:57:42.379160'),
(16, 'admin', '0001_initial', '2023-11-30 21:57:42.579728'),
(17, 'admin', '0002_logentry_remove_auto_add', '2023-11-30 21:57:42.595356'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2023-11-30 21:57:42.595356'),
(19, 'inventario', '0001_initial', '2023-11-30 21:57:42.965137'),
(20, 'metrologia', '0001_initial', '2023-11-30 21:57:43.466480'),
(21, 'calibracion', '0001_initial', '2023-11-30 21:57:43.513336'),
(22, 'calibracion', '0002_initial', '2023-11-30 21:57:43.829825'),
(23, 'calibracion', '0003_initial', '2023-11-30 21:57:43.914494'),
(24, 'inventario', '0002_initial', '2023-11-30 21:57:44.647628'),
(25, 'mantenimiento', '0001_initial', '2023-11-30 21:57:44.901670'),
(26, 'mantenimiento', '0002_initial', '2023-11-30 21:57:45.302896'),
(27, 'sessions', '0001_initial', '2023-11-30 21:57:45.418790'),
(28, 'verificacion', '0001_initial', '2023-11-30 21:57:45.919953'),
(29, 'mantenimiento', '0003_alter_especificacionmantenimiento_estado', '2023-12-01 17:44:41.136383'),
(30, 'calibracion', '0004_alter_especificacioncalibracion_estatus_and_more', '2023-12-01 21:33:03.585184'),
(31, 'verificacion', '0002_alter_especificacionverificacion_estatus_and_more', '2023-12-01 21:56:04.721161'),
(32, 'calibracion', '0005_alter_criterioscalibracion_valor', '2023-12-04 16:11:47.439256'),
(33, 'metrologia', '0002_alter_criteriosmetrologicos_valor_esperado', '2023-12-04 16:11:47.539562'),
(34, 'inventario', '0003_detalledocs_delete_docs_delete_tipodoc', '2023-12-04 17:43:56.107098'),
(35, 'inventario', '0004_alter_detalledocs_url', '2023-12-04 18:27:17.591970');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('w3te3c3cb32s91f3v1qpkpq6vmjn2fzz', '.eJxVjMEOwiAQBf-FsyGlhQKejHe_odldaEFr0UITE-O_2yY96OVdZua9WQdLCd2S_dxFx47sMQOVSJAFD9HBOKQTRSj-ye8vdvjVEejmp61xV5iGxClNZY7IN4XvNPNLcn487-7fQYAc1toaNKStlCBxHaFVZZqqcUKqHklLr6Tue7QIklDUZACr2rfOSCuEah37fAFf0kIs:1rAEgP:_HpzNTMd3l-__ULZZARJuEqKnF9sAs7dMOko0YgVulg', '2023-12-18 19:32:45.870532');

-- --------------------------------------------------------

--
-- Table structure for table `inventario_baja`
--

CREATE TABLE `inventario_baja` (
  `id` bigint(20) NOT NULL,
  `motivos` longtext NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `id_aprueba_id` varchar(254) NOT NULL,
  `id_equipo_id` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inventario_baja`
--

INSERT INTO `inventario_baja` (`id`, `motivos`, `fecha`, `id_aprueba_id`, `id_equipo_id`) VALUES
(1, '<textarea name=\"motivos\" cols=\"40\" rows=\"10\" required id=\"id_motivos\">', '2023-12-01 22:23:23.480753', 'practicas1.hidalgo@ciateq.mx', 'MD-E-0001-I-JL'),
(3, '<textarea name=\"motivos\" cols=\"40\" rows=\"10\" required id=\"id_motivos\">', '2023-12-04 20:18:05.314958', 'practicas1.hidalgo@ciateq.mx', 'IP-D-0001-I-EM');

-- --------------------------------------------------------

--
-- Table structure for table `inventario_clasificacion`
--

CREATE TABLE `inventario_clasificacion` (
  `id` varchar(1) NOT NULL,
  `nombre` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inventario_clasificacion`
--

INSERT INTO `inventario_clasificacion` (`id`, `nombre`) VALUES
('A', 'Accesorio'),
('I', 'Instrumento'),
('M', 'Maquina'),
('P', 'Patron');

-- --------------------------------------------------------

--
-- Table structure for table `inventario_detalledocs`
--

CREATE TABLE `inventario_detalledocs` (
  `id` bigint(20) NOT NULL,
  `url` varchar(100) NOT NULL,
  `id_equipo_id` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inventario_detalledocs`
--

INSERT INTO `inventario_detalledocs` (`id`, `url`, `id_equipo_id`) VALUES
(5, 'docs/inventario/modificarEquipo.html', 'IV-D-0001-A-AS'),
(6, 'docs/inventario/metrologia_detallecontrolmetro.sql_IV-D-0001-I-JL.sql', 'IV-D-0001-I-JL'),
(7, 'docs/inventario/IV-D-0002-I-JL_metrologia_detallecontrolmetro.sql', 'IV-D-0002-I-JL'),
(8, 'docs/inventario/IV-D-0003-I-JL_metrologia_detallecontrolmetro.sql', 'IV-D-0003-I-JL'),
(9, 'docs/inventario/IV-D-0003-I-JL_modificarEquipo.html', 'IV-D-0003-I-JL'),
(10, 'docs/inventario/IV-D-0003-I-JL_views_1.py', 'IV-D-0003-I-JL'),
(11, 'docs/inventario/LS-F-0001-I-HI_Detalles_de_equipo_LS-G-0001-M-JL.pdf', 'LS-F-0001-I-HI'),
(12, 'docs/inventario/LS-F-0001-I-HI_Detalles_de_equipo_IV-E-0001-P-HI.pdf', 'LS-F-0001-I-HI'),
(13, 'docs/inventario/LS-F-0001-I-HI_Detalles_de_equipo_LS-G-0001-M-JL_6Ip9jlx.pdf', 'LS-F-0001-I-HI'),
(14, 'docs/inventario/LS-F-0001-I-HI_Detalles_de_equipo_IV-E-0001-P-HI_gtst9MQ.pdf', 'LS-F-0001-I-HI'),
(15, 'docs/inventario/LS-F-0001-I-HI_modificarEquipo.html', 'LS-F-0001-I-HI');

-- --------------------------------------------------------

--
-- Table structure for table `inventario_direccionespecialidad`
--

CREATE TABLE `inventario_direccionespecialidad` (
  `id` varchar(4) NOT NULL,
  `nombre` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inventario_direccionespecialidad`
--

INSERT INTO `inventario_direccionespecialidad` (`id`, `nombre`) VALUES
('IP', 'Ingeniería De Plantas'),
('IV', 'Ingeniería Virtual Y Manufactura'),
('LS', 'Laboratorios'),
('MD', 'Sistemas de Medición'),
('PM', 'Plásticos Y Materiales Avanzados'),
('SM', 'Sistemas Mecánicos'),
('TT', 'TI- Electrónica Y  Control');

-- --------------------------------------------------------

--
-- Table structure for table `inventario_equipo`
--

CREATE TABLE `inventario_equipo` (
  `id` varchar(20) NOT NULL,
  `activo_fijo` varchar(10) DEFAULT NULL,
  `nombre_eq` varchar(100) NOT NULL,
  `marca` varchar(20) NOT NULL,
  `modelo` varchar(30) NOT NULL,
  `n_serie` varchar(30) NOT NULL,
  `accesorios` varchar(100) DEFAULT NULL,
  `codigo_qr` varchar(100) DEFAULT NULL,
  `imagen` varchar(100) DEFAULT NULL,
  `estatus` varchar(10) NOT NULL,
  `fecha_alta` date NOT NULL,
  `id_clasificacion_id` varchar(1) NOT NULL,
  `id_direccion_esp_id` varchar(4) NOT NULL,
  `id_magnitud_id` varchar(1) NOT NULL,
  `id_responsable_id` varchar(254) NOT NULL,
  `id_responsable_alta_id` varchar(254) NOT NULL,
  `id_sede_id` varchar(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inventario_equipo`
--

INSERT INTO `inventario_equipo` (`id`, `activo_fijo`, `nombre_eq`, `marca`, `modelo`, `n_serie`, `accesorios`, `codigo_qr`, `imagen`, `estatus`, `fecha_alta`, `id_clasificacion_id`, `id_direccion_esp_id`, `id_magnitud_id`, `id_responsable_id`, `id_responsable_alta_id`, `id_sede_id`) VALUES
('IP-D-0001-I-AS', NULL, 'RUGOSIMETRO', 'FLUKE', 'no se', '116929', 'ddd', 'imgs/inventario/QR/IP-D-0001-I-AS.png', 'imgs/inventario/equipos/IP-D-0001-I-AS.png', 'Activo', '2023-12-04', 'I', 'IP', 'D', 'practicas2.hidalgo@ciateq.mx', 'practicas2.hidalgo@ciateq.mx', 'AS'),
('IP-D-0001-I-EM', NULL, 'TERMÓMETRO CON ZONDA', 'FLUKE', '329-711-30', '79730207', 'ddd', 'imgs/inventario/QR/IP-D-0001-I-EM.png', 'IP-D-0001-I-EM.jpg', 'Baja', '2023-12-04', 'I', 'IP', 'D', 'practicas2.hidalgo@ciateq.mx', 'practicas2.hidalgo@ciateq.mx', 'EM'),
('IP-D-0001-I-QR', 'DFFDF', 'RUGOSIMETRO', 'no se', '329-711-30', '79730207', 'ddd', 'imgs/inventario/QR/IP-D-0001-I-QR.png', 'imgs/inventario/equipos/IP-D-0001-I-QR.jpg', 'Activo', '2023-12-04', 'I', 'IP', 'D', 'practicas1.hidalgo@ciateq.mx', 'practicas2.hidalgo@ciateq.mx', 'QR'),
('IP-D-0002-I-EM', NULL, 'TERMÓMETRO CON ZONDA', 'FLUKE', '329-711-30', '79730207', 'ddd', 'imgs/inventario/QR/IP-D-0002-I-EM.png', 'imgs/inventario/equipos/IP-D-0002-I-EM.jpg', 'Activo', '2023-12-04', 'I', 'IP', 'D', 'practicas2.hidalgo@ciateq.mx', 'practicas2.hidalgo@ciateq.mx', 'EM'),
('IP-D-0002-I-QR', 'DFFDF', 'RUGOSIMETRO', 'no se', '329-711-30', '79730207', 'ddd', 'imgs/inventario/QR/IP-D-0002-I-QR.png', 'imgs/inventario/equipos/IP-D-0002-I-QR.jpg', 'Activo', '2023-12-04', 'I', 'IP', 'D', 'practicas1.hidalgo@ciateq.mx', 'practicas2.hidalgo@ciateq.mx', 'QR'),
('IP-D-0003-I-EM', NULL, 'TERMÓMETRO CON ZONDA', 'FLUKE', '329-711-30', '79730207', 'ddd', 'imgs/inventario/QR/IP-D-0003-I-EM.png', 'imgs/inventario/equipos/IP-D-0003-I-EM.jpg', 'Activo', '2023-12-04', 'I', 'IP', 'D', 'practicas2.hidalgo@ciateq.mx', 'practicas2.hidalgo@ciateq.mx', 'EM'),
('IP-D-0003-I-QR', 'DFFDF', 'RUGOSIMETRO', 'no se', '329-711-30', '79730207', 'ddd', 'imgs/inventario/QR/IP-D-0003-I-QR.png', 'imgs/inventario/equipos/IP-D-0003-I-QR.jpg', 'Activo', '2023-12-04', 'I', 'IP', 'D', 'practicas1.hidalgo@ciateq.mx', 'practicas2.hidalgo@ciateq.mx', 'QR'),
('IP-D-0004-I-EM', NULL, 'TERMÓMETRO CON ZONDA', 'FLUKE', '329-711-30', '79730207', 'ddd', 'imgs/inventario/QR/IP-D-0004-I-EM.png', 'imgs/inventario/equipos/IP-D-0004-I-EM.jpg', 'Activo', '2023-12-04', 'I', 'IP', 'D', 'practicas2.hidalgo@ciateq.mx', 'practicas2.hidalgo@ciateq.mx', 'EM'),
('IP-D-0004-I-QR', 'DFFDF', 'RUGOSIMETRO', 'no se', '329-711-30', '79730207', 'ddd', 'imgs/inventario/QR/IP-D-0004-I-QR.png', 'imgs/inventario/equipos/IP-D-0004-I-QR.jpg', 'Activo', '2023-12-04', 'I', 'IP', 'D', 'practicas1.hidalgo@ciateq.mx', 'practicas2.hidalgo@ciateq.mx', 'QR'),
('IP-D-0005-I-EM', NULL, 'TERMÓMETRO CON ZONDA', 'FLUKE', '329-711-30', '79730207', 'ddd', 'imgs/inventario/QR/IP-D-0005-I-EM.png', 'imgs/inventario/equipos/IP-D-0005-I-EM.jpg', 'Activo', '2023-12-04', 'I', 'IP', 'D', 'practicas2.hidalgo@ciateq.mx', 'practicas2.hidalgo@ciateq.mx', 'EM'),
('IP-D-0005-I-QR', 'DFFDF', 'RUGOSIMETRO', 'no se', '329-711-30', '79730207', 'ddd', 'imgs/inventario/QR/IP-D-0005-I-QR.png', 'imgs/inventario/equipos/IP-D-0005-I-QR.jpg', 'Activo', '2023-12-04', 'I', 'IP', 'D', 'practicas1.hidalgo@ciateq.mx', 'practicas2.hidalgo@ciateq.mx', 'QR'),
('IP-D-0006-I-EM', NULL, 'TERMÓMETRO CON ZONDA', 'FLUKE', '329-711-30', '79730207', 'ddd', 'imgs/inventario/QR/IP-D-0006-I-EM.png', '', 'Activo', '2023-12-04', 'I', 'IP', 'D', 'practicas2.hidalgo@ciateq.mx', 'practicas2.hidalgo@ciateq.mx', 'EM'),
('IP-D-0006-I-QR', 'DFFDF', 'RUGOSIMETRO', 'no se', '329-711-30', '79730207', 'ddd', 'imgs/inventario/QR/IP-D-0006-I-QR.png', '', 'Activo', '2023-12-04', 'I', 'IP', 'D', 'practicas1.hidalgo@ciateq.mx', 'practicas2.hidalgo@ciateq.mx', 'QR'),
('IP-D-0007-I-QR', 'DFFDF', 'RUGOSIMETRO', 'no se', '329-711-30', '79730207', 'ddd', 'imgs/inventario/QR/IP-D-0007-I-QR.png', '', 'Activo', '2023-12-04', 'I', 'IP', 'D', 'practicas1.hidalgo@ciateq.mx', 'practicas2.hidalgo@ciateq.mx', 'QR'),
('IP-D-0008-I-QR', 'DFFDF', 'RUGOSIMETRO', 'no se', '329-711-30', '79730207', 'ddd', 'imgs/inventario/QR/IP-D-0008-I-QR.png', '', 'Activo', '2023-12-04', 'I', 'IP', 'D', 'practicas1.hidalgo@ciateq.mx', 'practicas2.hidalgo@ciateq.mx', 'QR'),
('IP-D-0009-I-QR', 'DFFDF', 'RUGOSIMETRO', 'no se', '329-711-30', '79730207', 'ddd', 'imgs/inventario/QR/IP-D-0009-I-QR.png', '', 'Activo', '2023-12-04', 'I', 'IP', 'D', 'practicas1.hidalgo@ciateq.mx', 'practicas2.hidalgo@ciateq.mx', 'QR'),
('IP-O-0001-I-EM', NULL, 'RUGOSIMETRO', 'ff', '52II', '79730207', 'ddd', 'imgs/inventario/QR/IP-O-0001-I-EM.png', 'imgs/inventario/equipos/IP-O-0001-I-EM.jpg', 'Activo', '2023-12-04', 'I', 'IP', 'O', 'practicas2.hidalgo@ciateq.mx', 'practicas2.hidalgo@ciateq.mx', 'EM'),
('IV-D-0001-A-AS', NULL, 'RUGOSIMETRO', 'FLUKE', 'gg', '79730207', 'ddd', 'imgs/inventario/QR/IV-D-0001-A-AS.png', 'imgs/inventario/equipos/IV-D-0001-A-AS.jpg', 'Activo', '2023-12-04', 'A', 'IV', 'D', 'practicas1.hidalgo@ciateq.mx', 'practicas2.hidalgo@ciateq.mx', 'AS'),
('IV-D-0001-I-JL', NULL, 'TERMÓMETRO CON ZONDA', 'FLUKE', '329-711-30', '116929', 'ddd', 'imgs/inventario/QR/IV-D-0001-I-JL.png', 'imgs/inventario/equipos/IV-D-0001-I-JL.jpg', 'Activo', '2023-12-04', 'I', 'IV', 'D', 'practicas1.hidalgo@ciateq.mx', 'practicas2.hidalgo@ciateq.mx', 'JL'),
('IV-D-0002-A-AS', NULL, 'RUGOSIMETRO', 'FLUKE', 'gg', '79730207', 'ddd', 'imgs/inventario/QR/IV-D-0002-A-AS.png', 'imgs/inventario/equipos/IV-D-0002-A-AS.jpg', 'Activo', '2023-12-04', 'A', 'IV', 'D', 'practicas1.hidalgo@ciateq.mx', 'practicas2.hidalgo@ciateq.mx', 'AS'),
('IV-D-0002-I-JL', NULL, 'TERMÓMETRO CON ZONDA', 'FLUKE', '329-711-30', '116929', 'ddd', 'imgs/inventario/QR/IV-D-0002-I-JL.png', 'imgs/inventario/equipos/IV-D-0002-I-JL.jpg', 'Activo', '2023-12-04', 'I', 'IV', 'D', 'practicas1.hidalgo@ciateq.mx', 'practicas2.hidalgo@ciateq.mx', 'JL'),
('IV-D-0003-A-AS', NULL, 'RUGOSIMETRO', 'FLUKE', 'gg', '79730207', 'ddd', 'imgs/inventario/QR/IV-D-0003-A-AS.png', 'imgs/inventario/equipos/IV-D-0003-A-AS.jpg', 'Activo', '2023-12-04', 'A', 'IV', 'D', 'practicas1.hidalgo@ciateq.mx', 'practicas2.hidalgo@ciateq.mx', 'AS'),
('IV-D-0003-I-JL', NULL, 'TERMÓMETRO CON ZONDA', 'FLUKE', '329-711-30', '116929', 'ddd', 'imgs/inventario/QR/IV-D-0003-I-JL.png', 'imgs/inventario/equipos/IV-D-0003-I-JL.jpg', 'Activo', '2023-12-04', 'I', 'IV', 'D', 'practicas1.hidalgo@ciateq.mx', 'practicas2.hidalgo@ciateq.mx', 'JL'),
('LS-D-0001-I-JL', NULL, 'TERMÓMETRO CON ZONDA', 'MITUTOYOr', 'no se', '79730207', 'ddd', 'imgs/inventario/QR/LS-D-0001-I-JL.png', 'imgs/inventario/equipos/LS-D-0001-I-JL.jpg', 'Activo', '2023-12-04', 'I', 'LS', 'D', 'practicas1.hidalgo@ciateq.mx', 'practicas1.hidalgo@ciateq.mx', 'JL'),
('LS-D-0002-I-JL', NULL, 'TERMÓMETRO CON ZONDA', 'MITUTOYOr', 'no se', '79730207', 'ddd', 'imgs/inventario/QR/LS-D-0002-I-JL.png', 'imgs/inventario/equipos/LS-D-0002-I-JL.jpg', 'Activo', '2023-12-04', 'I', 'LS', 'D', 'practicas1.hidalgo@ciateq.mx', 'practicas1.hidalgo@ciateq.mx', 'JL'),
('LS-F-0001-I-HI', NULL, 'RUGOSIMETRO', 'no se', '52II', 'dd', 'ddd', 'imgs/inventario/QR/LS-F-0001-I-HI.png', 'imgs/inventario/equipos/LS-F-0001-I-HI.jpg', 'Activo', '2023-12-04', 'I', 'LS', 'F', 'practicas1.hidalgo@ciateq.mx', 'practicas1.hidalgo@ciateq.mx', 'HI'),
('MD-E-0001-I-JL', NULL, 'RUGOSIMETRO', 'FLUKE', 'no se', '116929', 'ddd', 'imgs/inventario/QR/MD-E-0001-I-JL.png', 'MD-E-0001-I-JL.jpg', 'Baja', '2023-12-01', 'I', 'MD', 'E', 'practicas1.hidalgo@ciateq.mx', 'practicas1.hidalgo@ciateq.mx', 'JL');

-- --------------------------------------------------------

--
-- Table structure for table `inventario_magnitud`
--

CREATE TABLE `inventario_magnitud` (
  `id` varchar(1) NOT NULL,
  `nombre` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inventario_magnitud`
--

INSERT INTO `inventario_magnitud` (`id`, `nombre`) VALUES
('A', 'Administrativo'),
('D', 'Dimensional'),
('E', 'Prueba de encendedor'),
('F', 'Flujo'),
('G', 'Metalografía '),
('H', 'Química Combinatoria'),
('I', 'Térmico Reológico'),
('J', 'Propiedades Mecánica'),
('L', 'Eléctrica'),
('M', 'Masa'),
('O', 'Par-torsional'),
('P', 'Presión'),
('Q', 'Química'),
('R', 'Otras Pruebas'),
('T', 'Temperatura'),
('U', 'Fuerza'),
('V', 'Volumen'),
('W', 'Tiempo Frecuencia'),
('x', 'Plásticos'),
('Z', 'Dureza');

-- --------------------------------------------------------

--
-- Table structure for table `inventario_sede`
--

CREATE TABLE `inventario_sede` (
  `id` varchar(2) NOT NULL,
  `nombre` varchar(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inventario_sede`
--

INSERT INTO `inventario_sede` (`id`, `nombre`) VALUES
('AS', 'Aguascalientes'),
('EM', 'Estado de México'),
('HI', 'Hidalgo'),
('JL', 'Jalisco'),
('QR', 'Querétaro'),
('SL', 'San Luis Potosí'),
('TA', 'Tabasco');

-- --------------------------------------------------------

--
-- Table structure for table `mantenimiento_detallemantenimientoexterno`
--

CREATE TABLE `mantenimiento_detallemantenimientoexterno` (
  `num_folio` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `proveedor` varchar(100) NOT NULL,
  `tipo_mant` varchar(10) NOT NULL,
  `comentario` longtext DEFAULT NULL,
  `evidencia` varchar(100) DEFAULT NULL,
  `id_especificacion_mant_id` varchar(20) NOT NULL,
  `id_responsable_cap_id` varchar(254) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mantenimiento_detallemantenimientoexterno`
--

INSERT INTO `mantenimiento_detallemantenimientoexterno` (`num_folio`, `fecha`, `proveedor`, `tipo_mant`, `comentario`, `evidencia`, `id_especificacion_mant_id`, `id_responsable_cap_id`) VALUES
(1, '2023-12-04', 'CIATEQ', 'Preventivo', 'r', '', 'IP-D-0005-I-QR', 'practicas1.hidalgo@ciateq.mx');

-- --------------------------------------------------------

--
-- Table structure for table `mantenimiento_detallemantenimientointerno`
--

CREATE TABLE `mantenimiento_detallemantenimientointerno` (
  `num_folio` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `tipo_mant` varchar(10) NOT NULL,
  `comentario` longtext DEFAULT NULL,
  `evidencia` varchar(100) DEFAULT NULL,
  `id_especificacion_mant_id` varchar(20) NOT NULL,
  `id_responsable_id` varchar(254) NOT NULL,
  `id_responsable_cap_id` varchar(254) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `mantenimiento_especificacionmantenimiento`
--

CREATE TABLE `mantenimiento_especificacionmantenimiento` (
  `id_equipo_id` varchar(20) NOT NULL,
  `periodo` int(11) NOT NULL,
  `tipo_periodo` varchar(10) NOT NULL,
  `tiempo_uso` double DEFAULT NULL,
  `ultima` date DEFAULT NULL,
  `proxima` date DEFAULT NULL,
  `estado` varchar(10) NOT NULL,
  `comentario` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mantenimiento_especificacionmantenimiento`
--

INSERT INTO `mantenimiento_especificacionmantenimiento` (`id_equipo_id`, `periodo`, `tipo_periodo`, `tiempo_uso`, `ultima`, `proxima`, `estado`, `comentario`) VALUES
('IP-D-0001-I-AS', 1, 'meses', NULL, NULL, NULL, 'Pendiente', ''),
('IP-D-0005-I-QR', 800, 'horas', NULL, NULL, NULL, 'Pendiente', '');

-- --------------------------------------------------------

--
-- Table structure for table `metrologia_criterio`
--

CREATE TABLE `metrologia_criterio` (
  `id` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `metrologia_criteriosmetrologicos`
--

CREATE TABLE `metrologia_criteriosmetrologicos` (
  `id` bigint(20) NOT NULL,
  `rango` varchar(10) NOT NULL,
  `id_criterio` varchar(20) NOT NULL,
  `valor_esperado` double NOT NULL,
  `id_controlMetro_id` varchar(20) NOT NULL,
  `id_unidad_criterio_id` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `metrologia_criteriosmetrologicos`
--

INSERT INTO `metrologia_criteriosmetrologicos` (`id`, `rango`, `id_criterio`, `valor_esperado`, `id_controlMetro_id`, `id_unidad_criterio_id`) VALUES
(65, 'Max', 'Error', 556, 'MD-E-0001-I-JL', 'bar'),
(66, 'Min', 'Incertidumbre', 4, 'MD-E-0001-I-JL', 'bar'),
(67, '=', 'Linealidad', 5, 'MD-E-0001-I-JL', 'kgf·m'),
(68, 'Max', 'Error', 1, 'LS-D-0001-I-JL', 'L'),
(69, 'Min', 'Incertidumbre', 899, 'LS-D-0001-I-JL', 'kgf·m'),
(70, '=', 'Linealidad', 5, 'LS-D-0001-I-JL', 'L/min'),
(71, '±', 'Repetibilidad', 5, 'LS-D-0001-I-JL', 'kgf'),
(72, '±', 'Error', 1, 'LS-D-0002-I-JL', '%'),
(73, '±', 'Incertidumbre', 852, 'LS-D-0002-I-JL', '%'),
(74, 'Max', 'Error', 5, 'IP-D-0001-I-AS', 'kgf'),
(75, 'Max', 'Incertidumbre', 5, 'IP-D-0001-I-AS', 'kgf·m');

-- --------------------------------------------------------

--
-- Table structure for table `metrologia_especificacionmetrologia`
--

CREATE TABLE `metrologia_especificacionmetrologia` (
  `id_equipo_id` varchar(20) NOT NULL,
  `res_unidades` varchar(25) DEFAULT NULL,
  `intervalo_medicion_unidades` varchar(30) NOT NULL,
  `unidades_id` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `metrologia_especificacionmetrologia`
--

INSERT INTO `metrologia_especificacionmetrologia` (`id_equipo_id`, `res_unidades`, `intervalo_medicion_unidades`, `unidades_id`) VALUES
('IP-D-0001-I-AS', '55', '55555', 'bar'),
('LS-D-0001-I-JL', '55', 'r', 'atm'),
('LS-D-0002-I-JL', '55', '55555', 'dyne'),
('MD-E-0001-I-JL', '55', '55555', 'atm');

-- --------------------------------------------------------

--
-- Table structure for table `metrologia_unidad`
--

CREATE TABLE `metrologia_unidad` (
  `id` varchar(10) NOT NULL,
  `nombre` varchar(35) NOT NULL,
  `id_magnitud_id` varchar(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `metrologia_unidad`
--

INSERT INTO `metrologia_unidad` (`id`, `nombre`, `id_magnitud_id`) VALUES
('%', 'Porcentaje', 'A'),
('A', 'Amperio', 'L'),
('atm', 'Atmósfera', 'P'),
('bar', 'Bar', 'P'),
('C', 'Coulomb', 'L'),
('cm', 'Centímetro', 'D'),
('dyne', 'Dine', 'U'),
('g', 'Gramo', 'Q'),
('g/cm³', 'Gramo por centímetro cúbico', 'x'),
('HRC', 'Dureza Rockwell C', 'Z'),
('HV', 'Dureza Vickers', 'Z'),
('Hz', 'Hertz', 'W'),
('K', 'Kelvin', 'T'),
('kg', 'Kilogramo', 'Q'),
('kgf', 'Kilogramo fuerza', 'U'),
('kgf·m', 'Kilogramo fuerza metro', 'O'),
('L', 'Litro', 'V'),
('L/min', 'Litro por minuto', 'F'),
('lbf', 'Libra fuerza', 'U'),
('lbf·ft', 'Libra fuerza pie', 'O'),
('m', 'Metro', 'D'),
('mm', 'Milímetro', 'D'),
('mm²', 'Milímetro cuadrado', 'G'),
('mol', 'Mol', 'Q'),
('mol/L', 'Mol por litro', 'H'),
('MPa', 'Megapascal', 'J'),
('m²', 'Metro cuadrado', 'G'),
('m³', 'Metro cúbico', 'V'),
('m³/s', 'Metro cúbico por segundo', 'F'),
('N', 'Newton', 'U'),
('N/mm²', 'Newton por milímetro cuadrado', 'J'),
('N·m', 'Newton metro', 'O'),
('Pa', 'Pascal', 'P'),
('Pa·s', 'Pascal segundo', 'I'),
('s', 'Segundo', 'W'),
('V', 'Voltio', 'L'),
('W', 'Vatio', 'L'),
('°C', 'Celsius', 'T'),
('°C/s', 'Grados Celsius por segundo', 'I'),
('°F', 'Fahrenheit', 'T'),
('°R', 'Rankine', 'T'),
('°Re', 'Réaumur', 'T'),
('µm', 'Micrómetro', 'G'),
('Ω', 'Ohmio', 'L');

-- --------------------------------------------------------

--
-- Table structure for table `usuarios_customuser`
--

CREATE TABLE `usuarios_customuser` (
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `email` varchar(254) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `apellido_p` varchar(30) NOT NULL,
  `apellido_m` varchar(30) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `usuarios_customuser`
--

INSERT INTO `usuarios_customuser` (`password`, `last_login`, `is_superuser`, `email`, `nombre`, `apellido_p`, `apellido_m`, `is_active`, `is_staff`, `date_joined`) VALUES
('pbkdf2_sha256$600000$8UFjtaTTVo5yeuU1CJjGy0$p1B7u+dsZoV6UOyRsETjcndV2+rbSuBsnRtys0s8jPk=', '2023-12-04 19:32:45.865635', 1, 'practicas1.hidalgo@ciateq.mx', 'Isaac', 'Reynoso', 'Aldana', 1, 1, '2023-11-30 22:00:26.000000'),
('pbkdf2_sha256$600000$pwyaBdccaDrNWJHoKupVPT$jkZtWBJ94k5dSbIxoetcoL7Y7xvuV71dyXf209ZLPQc=', '2023-12-04 19:32:37.591880', 0, 'practicas2.hidalgo@ciateq.mx', 'Fernando Jesús', 'Cruz', 'Moreno', 1, 0, '2023-12-04 16:35:22.077416');

-- --------------------------------------------------------

--
-- Table structure for table `usuarios_customuser_groups`
--

CREATE TABLE `usuarios_customuser_groups` (
  `id` bigint(20) NOT NULL,
  `customuser_id` varchar(254) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `usuarios_customuser_groups`
--

INSERT INTO `usuarios_customuser_groups` (`id`, `customuser_id`, `group_id`) VALUES
(1, 'practicas1.hidalgo@ciateq.mx', 1),
(2, 'practicas2.hidalgo@ciateq.mx', 2);

-- --------------------------------------------------------

--
-- Table structure for table `usuarios_customuser_user_permissions`
--

CREATE TABLE `usuarios_customuser_user_permissions` (
  `id` bigint(20) NOT NULL,
  `customuser_id` varchar(254) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `usuarios_customuser_user_permissions`
--

INSERT INTO `usuarios_customuser_user_permissions` (`id`, `customuser_id`, `permission_id`) VALUES
(1, 'practicas1.hidalgo@ciateq.mx', 1),
(2, 'practicas1.hidalgo@ciateq.mx', 2),
(3, 'practicas1.hidalgo@ciateq.mx', 3),
(4, 'practicas1.hidalgo@ciateq.mx', 4),
(5, 'practicas1.hidalgo@ciateq.mx', 5),
(6, 'practicas1.hidalgo@ciateq.mx', 6),
(7, 'practicas1.hidalgo@ciateq.mx', 7),
(8, 'practicas1.hidalgo@ciateq.mx', 8),
(9, 'practicas1.hidalgo@ciateq.mx', 9),
(10, 'practicas1.hidalgo@ciateq.mx', 10),
(11, 'practicas1.hidalgo@ciateq.mx', 11),
(12, 'practicas1.hidalgo@ciateq.mx', 12),
(13, 'practicas1.hidalgo@ciateq.mx', 13),
(14, 'practicas1.hidalgo@ciateq.mx', 14),
(15, 'practicas1.hidalgo@ciateq.mx', 15),
(16, 'practicas1.hidalgo@ciateq.mx', 16),
(17, 'practicas1.hidalgo@ciateq.mx', 17),
(18, 'practicas1.hidalgo@ciateq.mx', 18),
(19, 'practicas1.hidalgo@ciateq.mx', 19),
(20, 'practicas1.hidalgo@ciateq.mx', 20),
(21, 'practicas1.hidalgo@ciateq.mx', 21),
(22, 'practicas1.hidalgo@ciateq.mx', 22),
(23, 'practicas1.hidalgo@ciateq.mx', 23),
(24, 'practicas1.hidalgo@ciateq.mx', 24),
(25, 'practicas1.hidalgo@ciateq.mx', 25),
(26, 'practicas1.hidalgo@ciateq.mx', 26),
(27, 'practicas1.hidalgo@ciateq.mx', 27),
(28, 'practicas1.hidalgo@ciateq.mx', 28),
(29, 'practicas1.hidalgo@ciateq.mx', 29),
(30, 'practicas1.hidalgo@ciateq.mx', 30),
(31, 'practicas1.hidalgo@ciateq.mx', 31),
(32, 'practicas1.hidalgo@ciateq.mx', 32),
(33, 'practicas1.hidalgo@ciateq.mx', 33),
(34, 'practicas1.hidalgo@ciateq.mx', 34),
(35, 'practicas1.hidalgo@ciateq.mx', 35),
(36, 'practicas1.hidalgo@ciateq.mx', 36),
(37, 'practicas1.hidalgo@ciateq.mx', 37),
(38, 'practicas1.hidalgo@ciateq.mx', 38),
(39, 'practicas1.hidalgo@ciateq.mx', 39),
(40, 'practicas1.hidalgo@ciateq.mx', 40),
(41, 'practicas1.hidalgo@ciateq.mx', 41),
(42, 'practicas1.hidalgo@ciateq.mx', 42),
(43, 'practicas1.hidalgo@ciateq.mx', 43),
(44, 'practicas1.hidalgo@ciateq.mx', 44),
(45, 'practicas1.hidalgo@ciateq.mx', 45),
(46, 'practicas1.hidalgo@ciateq.mx', 46),
(47, 'practicas1.hidalgo@ciateq.mx', 47),
(48, 'practicas1.hidalgo@ciateq.mx', 48),
(49, 'practicas1.hidalgo@ciateq.mx', 49),
(50, 'practicas1.hidalgo@ciateq.mx', 50),
(51, 'practicas1.hidalgo@ciateq.mx', 51),
(52, 'practicas1.hidalgo@ciateq.mx', 52),
(53, 'practicas1.hidalgo@ciateq.mx', 53),
(54, 'practicas1.hidalgo@ciateq.mx', 54),
(55, 'practicas1.hidalgo@ciateq.mx', 55),
(56, 'practicas1.hidalgo@ciateq.mx', 56),
(57, 'practicas1.hidalgo@ciateq.mx', 57),
(58, 'practicas1.hidalgo@ciateq.mx', 58),
(59, 'practicas1.hidalgo@ciateq.mx', 59),
(60, 'practicas1.hidalgo@ciateq.mx', 60),
(61, 'practicas1.hidalgo@ciateq.mx', 61),
(62, 'practicas1.hidalgo@ciateq.mx', 62),
(63, 'practicas1.hidalgo@ciateq.mx', 63),
(64, 'practicas1.hidalgo@ciateq.mx', 64),
(65, 'practicas1.hidalgo@ciateq.mx', 65),
(66, 'practicas1.hidalgo@ciateq.mx', 66),
(67, 'practicas1.hidalgo@ciateq.mx', 67),
(68, 'practicas1.hidalgo@ciateq.mx', 68),
(69, 'practicas1.hidalgo@ciateq.mx', 69),
(70, 'practicas1.hidalgo@ciateq.mx', 70),
(71, 'practicas1.hidalgo@ciateq.mx', 71),
(72, 'practicas1.hidalgo@ciateq.mx', 72),
(73, 'practicas1.hidalgo@ciateq.mx', 73),
(74, 'practicas1.hidalgo@ciateq.mx', 74),
(75, 'practicas1.hidalgo@ciateq.mx', 75),
(76, 'practicas1.hidalgo@ciateq.mx', 76),
(77, 'practicas1.hidalgo@ciateq.mx', 77),
(78, 'practicas1.hidalgo@ciateq.mx', 78),
(79, 'practicas1.hidalgo@ciateq.mx', 79),
(80, 'practicas1.hidalgo@ciateq.mx', 80),
(81, 'practicas1.hidalgo@ciateq.mx', 81),
(82, 'practicas1.hidalgo@ciateq.mx', 82),
(83, 'practicas1.hidalgo@ciateq.mx', 83),
(84, 'practicas1.hidalgo@ciateq.mx', 84),
(85, 'practicas1.hidalgo@ciateq.mx', 85),
(86, 'practicas1.hidalgo@ciateq.mx', 86),
(87, 'practicas1.hidalgo@ciateq.mx', 87),
(88, 'practicas1.hidalgo@ciateq.mx', 88),
(89, 'practicas1.hidalgo@ciateq.mx', 89),
(90, 'practicas1.hidalgo@ciateq.mx', 90),
(91, 'practicas1.hidalgo@ciateq.mx', 91),
(92, 'practicas1.hidalgo@ciateq.mx', 92),
(93, 'practicas1.hidalgo@ciateq.mx', 93),
(94, 'practicas1.hidalgo@ciateq.mx', 94),
(95, 'practicas1.hidalgo@ciateq.mx', 95),
(96, 'practicas1.hidalgo@ciateq.mx', 96),
(97, 'practicas1.hidalgo@ciateq.mx', 97),
(98, 'practicas1.hidalgo@ciateq.mx', 98),
(99, 'practicas1.hidalgo@ciateq.mx', 99),
(100, 'practicas1.hidalgo@ciateq.mx', 100),
(101, 'practicas1.hidalgo@ciateq.mx', 101),
(102, 'practicas1.hidalgo@ciateq.mx', 102),
(103, 'practicas1.hidalgo@ciateq.mx', 103),
(104, 'practicas1.hidalgo@ciateq.mx', 104);

-- --------------------------------------------------------

--
-- Table structure for table `verificacion_especificacionverificacion`
--

CREATE TABLE `verificacion_especificacionverificacion` (
  `id_equipo_id` varchar(20) NOT NULL,
  `periodo` int(11) NOT NULL,
  `ultima` date DEFAULT NULL,
  `proxima` date DEFAULT NULL,
  `estatus` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `verificacion_especificacionverificacion`
--

INSERT INTO `verificacion_especificacionverificacion` (`id_equipo_id`, `periodo`, `ultima`, `proxima`, `estatus`) VALUES
('IP-D-0001-I-AS', 2, NULL, NULL, 'Pendiente');

-- --------------------------------------------------------

--
-- Table structure for table `verificacion_verificacion`
--

CREATE TABLE `verificacion_verificacion` (
  `num_informe` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `puntoVer1` double DEFAULT NULL,
  `puntoVer2` double DEFAULT NULL,
  `puntoVer3` double DEFAULT NULL,
  `puntoVer4` double DEFAULT NULL,
  `puntoVer5` double DEFAULT NULL,
  `lecEq1` double DEFAULT NULL,
  `lecEq2` double DEFAULT NULL,
  `lecEq3` double DEFAULT NULL,
  `lecEq4` double DEFAULT NULL,
  `lecEq5` double DEFAULT NULL,
  `lecPatron1` double DEFAULT NULL,
  `lecPatron2` double DEFAULT NULL,
  `lecPatron3` double DEFAULT NULL,
  `lecPatron4` double DEFAULT NULL,
  `lecPatron5` double DEFAULT NULL,
  `errorVer1` double DEFAULT NULL,
  `errorVer2` double DEFAULT NULL,
  `errorVer3` double DEFAULT NULL,
  `errorVer4` double DEFAULT NULL,
  `errorVer5` double DEFAULT NULL,
  `dictamen` varchar(11) NOT NULL,
  `doc` varchar(100) DEFAULT NULL,
  `id_aprobación_id` varchar(254) NOT NULL,
  `id_patron_id` varchar(20) NOT NULL,
  `id_responsable_id` varchar(254) NOT NULL,
  `id_verificacion_id` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `calibracion_calibracion`
--
ALTER TABLE `calibracion_calibracion`
  ADD PRIMARY KEY (`cod_cer_cal`),
  ADD KEY `calibracion_calibrac_id_especificacion_id_8d273824_fk_calibraci` (`id_especificacion_id`),
  ADD KEY `calibracion_calibrac_resp_cap_id_87f45a03_fk_usuarios_` (`resp_cap_id`);

--
-- Indexes for table `calibracion_criterioscalibracion`
--
ALTER TABLE `calibracion_criterioscalibracion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `calibracion_criterio_cod_cer_cal_id_dcea84e2_fk_calibraci` (`cod_cer_cal_id`),
  ADD KEY `calibracion_criterio_id_criterio_id_f1f6c0b8_fk_metrologi` (`id_criterio_id`);

--
-- Indexes for table `calibracion_especificacioncalibracion`
--
ALTER TABLE `calibracion_especificacioncalibracion`
  ADD PRIMARY KEY (`id_equipo_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_usuarios_customuser_email` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `inventario_baja`
--
ALTER TABLE `inventario_baja`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id_equipo_id` (`id_equipo_id`),
  ADD KEY `inventario_baja_id_aprueba_id_eb9e9789_fk_usuarios_` (`id_aprueba_id`);

--
-- Indexes for table `inventario_clasificacion`
--
ALTER TABLE `inventario_clasificacion`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `inventario_detalledocs`
--
ALTER TABLE `inventario_detalledocs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `inventario_detalledo_id_equipo_id_52da6cc3_fk_inventari` (`id_equipo_id`);

--
-- Indexes for table `inventario_direccionespecialidad`
--
ALTER TABLE `inventario_direccionespecialidad`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `inventario_equipo`
--
ALTER TABLE `inventario_equipo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `inventario_equipo_id_clasificacion_id_4bd9293a_fk_inventari` (`id_clasificacion_id`),
  ADD KEY `inventario_equipo_id_direccion_esp_id_37bb8d8d_fk_inventari` (`id_direccion_esp_id`),
  ADD KEY `inventario_equipo_id_magnitud_id_418d67e5_fk_inventari` (`id_magnitud_id`),
  ADD KEY `inventario_equipo_id_responsable_id_5bd8c8a0_fk_usuarios_` (`id_responsable_id`),
  ADD KEY `inventario_equipo_id_responsable_alta__8ef6c732_fk_usuarios_` (`id_responsable_alta_id`),
  ADD KEY `inventario_equipo_id_sede_id_1f5e5aaa_fk_inventario_sede_id` (`id_sede_id`);

--
-- Indexes for table `inventario_magnitud`
--
ALTER TABLE `inventario_magnitud`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `inventario_sede`
--
ALTER TABLE `inventario_sede`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `mantenimiento_detallemantenimientoexterno`
--
ALTER TABLE `mantenimiento_detallemantenimientoexterno`
  ADD PRIMARY KEY (`num_folio`),
  ADD KEY `mantenimiento_detall_id_especificacion_ma_7649309a_fk_mantenimi` (`id_especificacion_mant_id`),
  ADD KEY `mantenimiento_detall_id_responsable_cap_i_6f6fa8a0_fk_usuarios_` (`id_responsable_cap_id`);

--
-- Indexes for table `mantenimiento_detallemantenimientointerno`
--
ALTER TABLE `mantenimiento_detallemantenimientointerno`
  ADD PRIMARY KEY (`num_folio`),
  ADD KEY `mantenimiento_detall_id_especificacion_ma_fd8bb8c2_fk_mantenimi` (`id_especificacion_mant_id`),
  ADD KEY `mantenimiento_detall_id_responsable_id_d03ab6e9_fk_usuarios_` (`id_responsable_id`),
  ADD KEY `mantenimiento_detall_id_responsable_cap_i_efbcdf8e_fk_usuarios_` (`id_responsable_cap_id`);

--
-- Indexes for table `mantenimiento_especificacionmantenimiento`
--
ALTER TABLE `mantenimiento_especificacionmantenimiento`
  ADD PRIMARY KEY (`id_equipo_id`);

--
-- Indexes for table `metrologia_criterio`
--
ALTER TABLE `metrologia_criterio`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `metrologia_criteriosmetrologicos`
--
ALTER TABLE `metrologia_criteriosmetrologicos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `metrologia_criterios_id_controlMetro_id_fefb1295_fk_metrologi` (`id_controlMetro_id`),
  ADD KEY `metrologia_criterios_id_unidad_criterio_i_2e2dd48e_fk_metrologi` (`id_unidad_criterio_id`);

--
-- Indexes for table `metrologia_especificacionmetrologia`
--
ALTER TABLE `metrologia_especificacionmetrologia`
  ADD PRIMARY KEY (`id_equipo_id`),
  ADD KEY `metrologia_especific_unidades_id_7fda4933_fk_metrologi` (`unidades_id`);

--
-- Indexes for table `metrologia_unidad`
--
ALTER TABLE `metrologia_unidad`
  ADD PRIMARY KEY (`id`),
  ADD KEY `metrologia_unidad_id_magnitud_id_05f38a91_fk_inventari` (`id_magnitud_id`);

--
-- Indexes for table `usuarios_customuser`
--
ALTER TABLE `usuarios_customuser`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `usuarios_customuser_groups`
--
ALTER TABLE `usuarios_customuser_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuarios_customuser_groups_customuser_id_group_id_aace3972_uniq` (`customuser_id`,`group_id`),
  ADD KEY `usuarios_customuser_groups_group_id_155d554c_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `usuarios_customuser_user_permissions`
--
ALTER TABLE `usuarios_customuser_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuarios_customuser_user_customuser_id_permission_8dac6e14_uniq` (`customuser_id`,`permission_id`),
  ADD KEY `usuarios_customuser__permission_id_9a10b097_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `verificacion_especificacionverificacion`
--
ALTER TABLE `verificacion_especificacionverificacion`
  ADD PRIMARY KEY (`id_equipo_id`);

--
-- Indexes for table `verificacion_verificacion`
--
ALTER TABLE `verificacion_verificacion`
  ADD PRIMARY KEY (`num_informe`),
  ADD KEY `verificacion_verific_id_aprobación_id_b44ef2ab_fk_usuarios_` (`id_aprobación_id`),
  ADD KEY `verificacion_verific_id_patron_id_216cf0c6_fk_inventari` (`id_patron_id`),
  ADD KEY `verificacion_verific_id_responsable_id_090fb4cc_fk_usuarios_` (`id_responsable_id`),
  ADD KEY `verificacion_verific_id_verificacion_id_c133e78a_fk_verificac` (`id_verificacion_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=109;

--
-- AUTO_INCREMENT for table `calibracion_criterioscalibracion`
--
ALTER TABLE `calibracion_criterioscalibracion`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `inventario_baja`
--
ALTER TABLE `inventario_baja`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `inventario_detalledocs`
--
ALTER TABLE `inventario_detalledocs`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `mantenimiento_detallemantenimientoexterno`
--
ALTER TABLE `mantenimiento_detallemantenimientoexterno`
  MODIFY `num_folio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `mantenimiento_detallemantenimientointerno`
--
ALTER TABLE `mantenimiento_detallemantenimientointerno`
  MODIFY `num_folio` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `metrologia_criteriosmetrologicos`
--
ALTER TABLE `metrologia_criteriosmetrologicos`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=76;

--
-- AUTO_INCREMENT for table `usuarios_customuser_groups`
--
ALTER TABLE `usuarios_customuser_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `usuarios_customuser_user_permissions`
--
ALTER TABLE `usuarios_customuser_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=105;

--
-- AUTO_INCREMENT for table `verificacion_verificacion`
--
ALTER TABLE `verificacion_verificacion`
  MODIFY `num_informe` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `calibracion_calibracion`
--
ALTER TABLE `calibracion_calibracion`
  ADD CONSTRAINT `calibracion_calibrac_id_especificacion_id_8d273824_fk_calibraci` FOREIGN KEY (`id_especificacion_id`) REFERENCES `calibracion_especificacioncalibracion` (`id_equipo_id`),
  ADD CONSTRAINT `calibracion_calibrac_resp_cap_id_87f45a03_fk_usuarios_` FOREIGN KEY (`resp_cap_id`) REFERENCES `usuarios_customuser` (`email`);

--
-- Constraints for table `calibracion_criterioscalibracion`
--
ALTER TABLE `calibracion_criterioscalibracion`
  ADD CONSTRAINT `calibracion_criterio_cod_cer_cal_id_dcea84e2_fk_calibraci` FOREIGN KEY (`cod_cer_cal_id`) REFERENCES `calibracion_calibracion` (`cod_cer_cal`),
  ADD CONSTRAINT `calibracion_criterio_id_criterio_id_f1f6c0b8_fk_metrologi` FOREIGN KEY (`id_criterio_id`) REFERENCES `metrologia_criteriosmetrologicos` (`id`);

--
-- Constraints for table `calibracion_especificacioncalibracion`
--
ALTER TABLE `calibracion_especificacioncalibracion`
  ADD CONSTRAINT `calibracion_especifi_id_equipo_id_0aa6a0dd_fk_inventari` FOREIGN KEY (`id_equipo_id`) REFERENCES `inventario_equipo` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_usuarios_customuser_email` FOREIGN KEY (`user_id`) REFERENCES `usuarios_customuser` (`email`);

--
-- Constraints for table `inventario_baja`
--
ALTER TABLE `inventario_baja`
  ADD CONSTRAINT `inventario_baja_id_aprueba_id_eb9e9789_fk_usuarios_` FOREIGN KEY (`id_aprueba_id`) REFERENCES `usuarios_customuser` (`email`),
  ADD CONSTRAINT `inventario_baja_id_equipo_id_ad4f51a9_fk_inventario_equipo_id` FOREIGN KEY (`id_equipo_id`) REFERENCES `inventario_equipo` (`id`);

--
-- Constraints for table `inventario_detalledocs`
--
ALTER TABLE `inventario_detalledocs`
  ADD CONSTRAINT `inventario_detalledo_id_equipo_id_52da6cc3_fk_inventari` FOREIGN KEY (`id_equipo_id`) REFERENCES `inventario_equipo` (`id`);

--
-- Constraints for table `inventario_equipo`
--
ALTER TABLE `inventario_equipo`
  ADD CONSTRAINT `inventario_equipo_id_clasificacion_id_4bd9293a_fk_inventari` FOREIGN KEY (`id_clasificacion_id`) REFERENCES `inventario_clasificacion` (`id`),
  ADD CONSTRAINT `inventario_equipo_id_direccion_esp_id_37bb8d8d_fk_inventari` FOREIGN KEY (`id_direccion_esp_id`) REFERENCES `inventario_direccionespecialidad` (`id`),
  ADD CONSTRAINT `inventario_equipo_id_magnitud_id_418d67e5_fk_inventari` FOREIGN KEY (`id_magnitud_id`) REFERENCES `inventario_magnitud` (`id`),
  ADD CONSTRAINT `inventario_equipo_id_responsable_alta__8ef6c732_fk_usuarios_` FOREIGN KEY (`id_responsable_alta_id`) REFERENCES `usuarios_customuser` (`email`),
  ADD CONSTRAINT `inventario_equipo_id_responsable_id_5bd8c8a0_fk_usuarios_` FOREIGN KEY (`id_responsable_id`) REFERENCES `usuarios_customuser` (`email`),
  ADD CONSTRAINT `inventario_equipo_id_sede_id_1f5e5aaa_fk_inventario_sede_id` FOREIGN KEY (`id_sede_id`) REFERENCES `inventario_sede` (`id`);

--
-- Constraints for table `mantenimiento_detallemantenimientoexterno`
--
ALTER TABLE `mantenimiento_detallemantenimientoexterno`
  ADD CONSTRAINT `mantenimiento_detall_id_especificacion_ma_7649309a_fk_mantenimi` FOREIGN KEY (`id_especificacion_mant_id`) REFERENCES `mantenimiento_especificacionmantenimiento` (`id_equipo_id`),
  ADD CONSTRAINT `mantenimiento_detall_id_responsable_cap_i_6f6fa8a0_fk_usuarios_` FOREIGN KEY (`id_responsable_cap_id`) REFERENCES `usuarios_customuser` (`email`);

--
-- Constraints for table `mantenimiento_detallemantenimientointerno`
--
ALTER TABLE `mantenimiento_detallemantenimientointerno`
  ADD CONSTRAINT `mantenimiento_detall_id_especificacion_ma_fd8bb8c2_fk_mantenimi` FOREIGN KEY (`id_especificacion_mant_id`) REFERENCES `mantenimiento_especificacionmantenimiento` (`id_equipo_id`),
  ADD CONSTRAINT `mantenimiento_detall_id_responsable_cap_i_efbcdf8e_fk_usuarios_` FOREIGN KEY (`id_responsable_cap_id`) REFERENCES `usuarios_customuser` (`email`),
  ADD CONSTRAINT `mantenimiento_detall_id_responsable_id_d03ab6e9_fk_usuarios_` FOREIGN KEY (`id_responsable_id`) REFERENCES `usuarios_customuser` (`email`);

--
-- Constraints for table `mantenimiento_especificacionmantenimiento`
--
ALTER TABLE `mantenimiento_especificacionmantenimiento`
  ADD CONSTRAINT `mantenimiento_especi_id_equipo_id_e65eeb27_fk_inventari` FOREIGN KEY (`id_equipo_id`) REFERENCES `inventario_equipo` (`id`);

--
-- Constraints for table `metrologia_criteriosmetrologicos`
--
ALTER TABLE `metrologia_criteriosmetrologicos`
  ADD CONSTRAINT `metrologia_criterios_id_controlMetro_id_fefb1295_fk_metrologi` FOREIGN KEY (`id_controlMetro_id`) REFERENCES `metrologia_especificacionmetrologia` (`id_equipo_id`),
  ADD CONSTRAINT `metrologia_criterios_id_unidad_criterio_i_2e2dd48e_fk_metrologi` FOREIGN KEY (`id_unidad_criterio_id`) REFERENCES `metrologia_unidad` (`id`);

--
-- Constraints for table `metrologia_especificacionmetrologia`
--
ALTER TABLE `metrologia_especificacionmetrologia`
  ADD CONSTRAINT `metrologia_especific_id_equipo_id_d496a38c_fk_inventari` FOREIGN KEY (`id_equipo_id`) REFERENCES `inventario_equipo` (`id`),
  ADD CONSTRAINT `metrologia_especific_unidades_id_7fda4933_fk_metrologi` FOREIGN KEY (`unidades_id`) REFERENCES `metrologia_unidad` (`id`);

--
-- Constraints for table `metrologia_unidad`
--
ALTER TABLE `metrologia_unidad`
  ADD CONSTRAINT `metrologia_unidad_id_magnitud_id_05f38a91_fk_inventari` FOREIGN KEY (`id_magnitud_id`) REFERENCES `inventario_magnitud` (`id`);

--
-- Constraints for table `usuarios_customuser_groups`
--
ALTER TABLE `usuarios_customuser_groups`
  ADD CONSTRAINT `usuarios_customuser__customuser_id_9e05d670_fk_usuarios_` FOREIGN KEY (`customuser_id`) REFERENCES `usuarios_customuser` (`email`),
  ADD CONSTRAINT `usuarios_customuser_groups_group_id_155d554c_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `usuarios_customuser_user_permissions`
--
ALTER TABLE `usuarios_customuser_user_permissions`
  ADD CONSTRAINT `usuarios_customuser__customuser_id_c016378e_fk_usuarios_` FOREIGN KEY (`customuser_id`) REFERENCES `usuarios_customuser` (`email`),
  ADD CONSTRAINT `usuarios_customuser__permission_id_9a10b097_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

--
-- Constraints for table `verificacion_especificacionverificacion`
--
ALTER TABLE `verificacion_especificacionverificacion`
  ADD CONSTRAINT `verificacion_especif_id_equipo_id_2f98e42b_fk_inventari` FOREIGN KEY (`id_equipo_id`) REFERENCES `inventario_equipo` (`id`);

--
-- Constraints for table `verificacion_verificacion`
--
ALTER TABLE `verificacion_verificacion`
  ADD CONSTRAINT `verificacion_verific_id_aprobación_id_b44ef2ab_fk_usuarios_` FOREIGN KEY (`id_aprobación_id`) REFERENCES `usuarios_customuser` (`email`),
  ADD CONSTRAINT `verificacion_verific_id_patron_id_216cf0c6_fk_inventari` FOREIGN KEY (`id_patron_id`) REFERENCES `inventario_equipo` (`id`),
  ADD CONSTRAINT `verificacion_verific_id_responsable_id_090fb4cc_fk_usuarios_` FOREIGN KEY (`id_responsable_id`) REFERENCES `usuarios_customuser` (`email`),
  ADD CONSTRAINT `verificacion_verific_id_verificacion_id_c133e78a_fk_verificac` FOREIGN KEY (`id_verificacion_id`) REFERENCES `verificacion_especificacionverificacion` (`id_equipo_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
