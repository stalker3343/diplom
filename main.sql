-- MySQL dump 10.13  Distrib 5.7.41, for Linux (x86_64)
--
-- Host: localhost    Database: main
-- ------------------------------------------------------
-- Server version	5.7.41-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (2,'Admin'),(1,'Users');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$390000$J8NUNB3g5vE8AAiuxzOJhe$qRZWSE7RVXmJBSbyJwXeKcKzHo54pwGkjhb5SQO7Tgo=','2023-05-09 17:32:11.846114',1,'support','','','',1,1,'2023-05-08 15:21:54.006584'),(2,'pbkdf2_sha256$390000$vZ5II7KvpQw18kjKkszqad$gfvZN6eqnuupDLBn+HIQQtCsl7uu5GhPmKHoIl2lybw=','2023-05-09 17:28:55.268094',0,'admin','','','',0,1,'2023-05-08 15:51:33.000000'),(3,'pbkdf2_sha256$390000$F5ey4SPmeeZfQdaHrI69ZX$X1Eqrnyfvb7QNw41GonZP1a2NFSum5sHb8YfECs8SpA=','2023-05-08 16:25:33.357222',0,'user','','','',0,1,'2023-05-08 15:52:08.000000');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (1,2,1),(2,2,2),(3,3,1);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2023-05-08 15:22:55.981486','1','InfectionRate object (1)',1,'[{\"added\": {}}]',1,1),(2,'2023-05-08 15:23:10.314479','2','InfectionRate object (2)',1,'[{\"added\": {}}]',1,1),(3,'2023-05-08 15:23:23.838390','1','Protocols object (1)',1,'[{\"added\": {}}]',2,1),(4,'2023-05-08 15:23:27.835306','2','Protocols object (2)',1,'[{\"added\": {}}]',2,1),(5,'2023-05-08 15:23:31.915286','3','Protocols object (3)',1,'[{\"added\": {}}]',2,1),(6,'2023-05-08 15:32:08.644045','1','Users object (1)',1,'[{\"added\": {}}]',4,1),(7,'2023-05-08 15:47:21.043235','1','CVES object (1)',1,'[{\"added\": {}}]',5,1),(8,'2023-05-08 15:48:22.128648','2','CVES object (2)',1,'[{\"added\": {}}]',5,1),(9,'2023-05-08 15:48:56.310597','3','CVES object (3)',1,'[{\"added\": {}}]',5,1),(10,'2023-05-08 15:49:31.591120','4','CVES object (4)',1,'[{\"added\": {}}]',5,1),(11,'2023-05-08 15:50:16.641356','5','CVES object (5)',1,'[{\"added\": {}}]',5,1),(12,'2023-05-08 15:51:03.064036','6','CVES object (6)',1,'[{\"added\": {}}]',5,1),(13,'2023-05-08 15:51:34.045829','2','admin',1,'[{\"added\": {}}]',6,1),(14,'2023-05-08 15:51:48.856812','2','admin',2,'[{\"changed\": {\"fields\": [\"Staff status\", \"Superuser status\"]}}]',6,1),(15,'2023-05-08 15:52:08.790167','3','user',1,'[{\"added\": {}}]',6,1),(16,'2023-05-08 15:52:32.141095','3','user',2,'[]',6,1),(17,'2023-05-08 15:53:23.686995','1','Users',1,'[{\"added\": {}}]',7,1),(18,'2023-05-08 15:53:31.607152','2','Admin',1,'[{\"added\": {}}]',7,1),(19,'2023-05-08 15:53:51.819171','2','Admin',2,'[]',7,1),(20,'2023-05-08 15:54:29.530937','2','admin',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',6,1),(21,'2023-05-08 15:54:40.787776','3','user',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',6,1),(22,'2023-05-08 15:58:44.773376','2','admin',2,'[{\"changed\": {\"fields\": [\"Staff status\", \"Superuser status\"]}}]',6,1),(23,'2023-05-08 16:00:34.292309','2','admin',2,'[]',6,1),(24,'2023-05-08 16:01:03.750787','2','admin',2,'[]',6,1),(25,'2023-05-08 18:29:41.320655','1','ResultScan object (1)',1,'[{\"added\": {}}]',3,1),(26,'2023-05-08 18:30:10.722680','2','ResultScan object (2)',1,'[{\"added\": {}}]',3,1),(27,'2023-05-09 15:56:12.973515','3','ResultScan object (3)',3,'',3,1),(28,'2023-05-09 16:13:10.283808','4','ResultScan object (4)',3,'',3,1),(29,'2023-05-09 16:13:55.539810','5','ResultScan object (5)',1,'[{\"added\": {}}]',3,1),(30,'2023-05-09 16:15:53.476526','5','ResultScan object (5)',3,'',3,1),(31,'2023-05-09 16:20:02.603868','3','ResultScan object (3)',1,'[{\"added\": {}}]',3,1),(32,'2023-05-09 16:20:07.729272','3','ResultScan object (3)',3,'',3,1),(33,'2023-05-09 16:20:29.604592','4','ResultScan object (4)',1,'[{\"added\": {}}]',3,1),(34,'2023-05-09 16:20:37.637238','4','ResultScan object (4)',3,'',3,1),(35,'2023-05-09 16:56:03.693112','6','ResultScan object (6)',3,'',3,1),(36,'2023-05-09 16:56:07.411591','5','ResultScan object (5)',3,'',3,1),(37,'2023-05-09 16:56:10.866807','4','ResultScan object (4)',3,'',3,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (7,'auth','group'),(6,'auth','user'),(5,'main','cves'),(1,'main','infectionrate'),(2,'main','protocols'),(3,'main','resultscan'),(4,'main','users');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2023-05-08 15:21:15.943685'),(2,'auth','0001_initial','2023-05-08 15:21:16.240990'),(3,'admin','0001_initial','2023-05-08 15:21:16.350100'),(4,'admin','0002_logentry_remove_auto_add','2023-05-08 15:21:16.381498'),(5,'admin','0003_logentry_add_action_flag_choices','2023-05-08 15:21:16.381498'),(6,'contenttypes','0002_remove_content_type_name','2023-05-08 15:21:16.474777'),(7,'auth','0002_alter_permission_name_max_length','2023-05-08 15:21:16.474777'),(8,'auth','0003_alter_user_email_max_length','2023-05-08 15:21:16.491172'),(9,'auth','0004_alter_user_username_opts','2023-05-08 15:21:16.506177'),(10,'auth','0005_alter_user_last_login_null','2023-05-08 15:21:16.521707'),(11,'auth','0006_require_contenttypes_0002','2023-05-08 15:21:16.521707'),(12,'auth','0007_alter_validators_add_error_messages','2023-05-08 15:21:16.537681'),(13,'auth','0008_alter_user_username_max_length','2023-05-08 15:21:16.553672'),(14,'auth','0009_alter_user_last_name_max_length','2023-05-08 15:21:16.568684'),(15,'auth','0010_alter_group_name_max_length','2023-05-08 15:21:16.584655'),(16,'auth','0011_update_proxy_permissions','2023-05-08 15:21:16.599764'),(17,'auth','0012_alter_user_first_name_max_length','2023-05-08 15:21:16.615630'),(18,'main','0001_initial','2023-05-08 15:21:16.693609'),(19,'sessions','0001_initial','2023-05-08 15:21:16.710020'),(20,'main','0002_alter_resultscan_scan_data_and_more','2023-05-08 15:27:59.150401'),(21,'main','0003_delete_users_alter_resultscan_scan_data','2023-05-08 15:46:08.814989'),(22,'main','0004_alter_resultscan_scan_data','2023-05-08 16:01:15.391976');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('ecm3ihz2di0vbfonubiopm2ymwl3zrcg','e30:1pw3jp:QmEakGyBGB_UMGbXokQYhL4PpSXTVDxx53Dg9tKzn-U','2023-05-22 16:29:25.091565'),('wfsli1994j8pujrmh97o859y7iqdkfwj','.eJxVjDkOwjAUBe_iGllegsOnpOcM1l9sHEC2FCcV4u4QKQW0b2beS0VclxLXnuY4iTorqw6_GyE_Ut2A3LHemuZWl3kivSl6p11fm6TnZXf_Dgr28q3JBGTODthmn0nEwOAFnTOjGdgSkQMwAgOOJ6BACUgCHYN11klir94fAuM4fA:1pwRC7:cgVwn2hCdI-mC5iOyZfwBujVrdTDpRf3mqpWnXMT1nk','2023-05-23 17:32:11.846114');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_cves`
--

DROP TABLE IF EXISTS `main_cves`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_cves` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `CVE_id` varchar(50) NOT NULL,
  `name` varchar(250) NOT NULL,
  `description` longtext NOT NULL,
  `CVSS` double NOT NULL,
  `protocol_id_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `main_cves_protocol_id_id_31872941_fk_main_protocols_id` (`protocol_id_id`),
  CONSTRAINT `main_cves_protocol_id_id_31872941_fk_main_protocols_id` FOREIGN KEY (`protocol_id_id`) REFERENCES `main_protocols` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_cves`
--

LOCK TABLES `main_cves` WRITE;
/*!40000 ALTER TABLE `main_cves` DISABLE KEYS */;
INSERT INTO `main_cves` VALUES (1,'CVE-2020-0609','BlueGate','Vulnerability allows an unauthenticated, restricted user to obtain remote code execution with the highest privileges through Remote Desktop Gateway for RDP',9.8,3),(2,'CVE-2020-0796','Samba Vulnerability','A remote code execution vulnerability exists in the way that the Microsoft Server Message Block 3.1.1 (SMBv3) protocol handles certain requests, aka \'Windows SMBv3 Client/Server Remote Code Execution Vulnerability\'.',10,1),(3,'CVE-2021-44142','SMBGhost','The Samba vfs_fruit module uses extended file attributes (EA, xattr) to provide \"...enhanced compatibility with Apple SMB clients and interoperability with a Netatalk 3 AFP fileserver.\" Samba versions prior to 4.13.17, 4.14.12 and 4.15.5 with vfs_fruit configured allow out-of-bounds heap read and write via specially crafted extended file attributes. A remote attacker with write access to extended file attributes can execute arbitrary code with the privileges of smbd, typically root.',8.8,1),(4,'CVE-2022-21907','SOCMAP','With a single iteration of the attack, the Windows device will restart and function normally but with continuous attack, this could lead to Denial of Service (DoS) conditions.',9.8,2),(5,'CVE-2022-41040','Vonahisec','a critical unauthenticated remote code execution vulnerability affecting at least 24 on-premise ManageEngine products. The vulnerability applies only if SAML SSO is enabled. For some products it also applies if SAML SSO was previously enabled.',9.8,2),(6,'CVE-2022-47966','CodeSetRelating','A server-side request forgery (SSRF) vulnerability',8.8,2);
/*!40000 ALTER TABLE `main_cves` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_infectionrate`
--

DROP TABLE IF EXISTS `main_infectionrate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_infectionrate` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `gradation` varchar(50) NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_infectionrate`
--

LOCK TABLES `main_infectionrate` WRITE;
/*!40000 ALTER TABLE `main_infectionrate` DISABLE KEYS */;
INSERT INTO `main_infectionrate` VALUES (1,'hign','A high level of infection gradation indicates a high probability of infiltrating the target device, thus exposing the risk of removing confidential information.'),(2,'low','A low level of infection gradation means that the target system is sufficiently resistant to threats from persons with limited access.');
/*!40000 ALTER TABLE `main_infectionrate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_protocols`
--

DROP TABLE IF EXISTS `main_protocols`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_protocols` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `protocol` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_protocols`
--

LOCK TABLES `main_protocols` WRITE;
/*!40000 ALTER TABLE `main_protocols` DISABLE KEYS */;
INSERT INTO `main_protocols` VALUES (1,'SMB'),(2,'HTTP'),(3,'RDP');
/*!40000 ALTER TABLE `main_protocols` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_resultscan`
--

DROP TABLE IF EXISTS `main_resultscan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_resultscan` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `ip_target` varchar(50) NOT NULL,
  `cve_id` varchar(50) NOT NULL,
  `protocol` varchar(10) NOT NULL,
  `scan_data` datetime(6) NOT NULL,
  `gradation` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_resultscan`
--

LOCK TABLES `main_resultscan` WRITE;
/*!40000 ALTER TABLE `main_resultscan` DISABLE KEYS */;
INSERT INTO `main_resultscan` VALUES (1,'192.168.220.135','CVE-2020-0609','RDP','2023-05-08 21:27:59.000000','low'),(2,'192.168.220.134','CVE-2022-21907','HTTP','2023-05-08 21:27:59.000000','hign'),(3,'192.168.220.87','CVE-2020-0609','RDP','2023-05-09 19:21:31.127226','hign'),(4,'192.168.220.87','CVE-2020-0609','RDP','2023-05-09 20:27:34.486844','hign');
/*!40000 ALTER TABLE `main_resultscan` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-08 19:44:32
