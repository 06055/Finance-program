-- MySQL dump 10.13  Distrib 8.1.0, for Win64 (x86_64)
--
-- Host: localhost    Database: home_finances
-- ------------------------------------------------------
-- Server version	8.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `actually_type_currency`
--

DROP TABLE IF EXISTS `actually_type_currency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actually_type_currency` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(10) NOT NULL,
  `money_type` varchar(10) NOT NULL,
  `money` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actually_type_currency`
--

LOCK TABLES `actually_type_currency` WRITE;
/*!40000 ALTER TABLE `actually_type_currency` DISABLE KEYS */;
/*!40000 ALTER TABLE `actually_type_currency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `parent_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Покупки',2),(2,'Планшет',3),(3,'Телефон',4),(5,'Повербанк',4),(6,'Одежда',5),(7,'Банан',1),(9,'Скутер',4),(10,'Браслет',4),(11,'Окорочка',6),(12,'Молоко',6),(13,'Покупки',6),(14,'ПриватБанк',8),(15,'Монобанк',8),(16,'Ощадбанк',8),(17,'Райффайзен Банк',8);
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `counterparties`
--

DROP TABLE IF EXISTS `counterparties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `counterparties` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `counterparties`
--

LOCK TABLES `counterparties` WRITE;
/*!40000 ALTER TABLE `counterparties` DISABLE KEYS */;
INSERT INTO `counterparties` VALUES (1,'Ашан'),(2,'Фора'),(3,'Фокстрот'),(4,'Розетка'),(5,'DreamTown'),(6,'Varus'),(8,'Банки');
/*!40000 ALTER TABLE `counterparties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pocket`
--

DROP TABLE IF EXISTS `pocket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pocket` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `type_pocket` varchar(64) NOT NULL,
  `type_currency` varchar(64) NOT NULL,
  `data_made` datetime DEFAULT NULL,
  `data_change` datetime DEFAULT NULL,
  `count_money` decimal(16,2) DEFAULT NULL,
  `bg_color` varchar(32) DEFAULT NULL,
  `bg_picture` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pocket`
--

LOCK TABLES `pocket` WRITE;
/*!40000 ALTER TABLE `pocket` DISABLE KEYS */;
INSERT INTO `pocket` VALUES (2,'privatcard','debit','EUR','2030-12-31 00:00:00',NULL,247733.00,'#e35e78',NULL),(3,'japancard','debit','EUR','2024-12-06 00:00:00',NULL,27478.00,NULL,'C://Finans_programm/images/background_card\\cat.png'),(4,'local card','kredit','UAH','2035-12-31 00:00:00',NULL,-2850.00,NULL,'C://Finans_programm/images/background_card\\LOGO_2.png'),(5,'PC','debit','UAH','2021-06-07 00:00:00',NULL,29985754.33,'#ff0000',NULL),(6,'visaUSD','debit','USD','2004-04-25 00:00:00',NULL,7800.00,NULL,'C://Finans_programm/images/background_card\\logo_py.png'),(9,'Server card','debit','USD','2011-01-13 00:00:00',NULL,16090.00,'#fbff42',NULL);
/*!40000 ALTER TABLE `pocket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subcategory`
--

DROP TABLE IF EXISTS `subcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subcategory` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `parent_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subcategory`
--

LOCK TABLES `subcategory` WRITE;
/*!40000 ALTER TABLE `subcategory` DISABLE KEYS */;
INSERT INTO `subcategory` VALUES (1,'Процессор',2),(2,'Зарядка',9),(3,'Бусины',10),(4,'Футболка',6),(5,'Шорты',6),(6,'Эмблема',6),(7,'Электроэнергия',14),(8,'Газ',14),(9,'Вода',14),(10,'Интернет',14),(11,'Аккамулятор',5);
/*!40000 ALTER TABLE `subcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `counteragent` varchar(255) NOT NULL,
  `categoria` varchar(255) NOT NULL,
  `subcategoria` varchar(255) NOT NULL,
  `type_transaction` varchar(50) NOT NULL,
  `count` decimal(10,2) NOT NULL,
  `currency` varchar(50) NOT NULL,
  `card` varchar(255) NOT NULL,
  `data` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (20,'Банки','ПриватБанк','Электроэнергия','Расход',-10000.00,'USD','visaUSD','2025-01-31'),(21,'Фокстрот','Планшет','Процессор','Расход',-1700.00,'EUR','privatcard','2025-01-26'),(22,'Банки','ПриватБанк','Электроэнергия','Доход',10000.00,'UAH','local card','2025-01-27'),(23,'Банки','ПриватБанк','Электроэнергия','Доход',150.00,'EUR','privatcard','2024-07-01'),(24,'Розетка','Скутер','Зарядка','Расход',-1500.67,'UAH','PC','2019-10-21'),(25,'DreamTown','Одежда','Шорты','Расход',-6000.00,'EUR','japancard','2025-01-06'),(26,'Розетка','Браслет','Бусины','Доход',500.00,'EUR','japancard','2025-01-05'),(27,'DreamTown','Одежда','Шорты','Доход',500.00,'EUR','japancard','2025-01-12'),(28,'Фокстрот','Планшет','Процессор','Доход',50.00,'EUR','privatcard','2025-01-25'),(29,'Банки','ПриватБанк','Газ','Расход',-155.00,'UAH','PC','2025-01-28'),(30,'Розетка','Браслет','Бусины','Расход',-777.00,'EUR','privatcard','2025-01-22'),(31,'DreamTown','Одежда','Футболка','Доход',8787.00,'EUR','japancard','2025-01-27'),(32,'Фокстрот','Планшет','Процессор','Расход',-9990.00,'UAH','PC','2025-01-28'),(33,'Банки','ПриватБанк','Вода','Расход',-20.00,'EUR','japancard','2025-02-05'),(34,'Банки','ПриватБанк','Газ','Расход',-19.00,'EUR','japancard','2025-02-28'),(35,'DreamTown','Одежда','Шорты','Расход',-1000.00,'UAH','PC','2025-02-03'),(36,'Розетка','Скутер','Зарядка','Доход',500.00,'UAH','PC','2025-02-03'),(37,'Розетка','Браслет','Бусины','Расход',-1000.00,'UAH','local card','2025-02-03'),(38,'Розетка','Скутер','Зарядка','Расход',-700.00,'USD','visaUSD','2025-02-24'),(39,'Розетка','Скутер','Зарядка','Расход',-800.00,'USD','Server card','2025-01-31'),(40,'DreamTown','Одежда','Шорты','Доход',900.00,'USD','Server card','2024-10-28'),(41,'Банки','ПриватБанк','Интернет','Доход',890.00,'USD','Server card','2025-02-03'),(42,'DreamTown','Одежда','Футболка','Расход',-600.00,'USD','Server card','2025-02-02'),(43,'DreamTown','Одежда','Футболка','Доход',500.00,'USD','Server card','2025-02-04'),(44,'Банки','ПриватБанк','Газ','Расход',-90.00,'USD','Server card','2025-01-14'),(45,'Банки','ПриватБанк','Вода','Расход',-10.00,'USD','Server card','2025-02-03'),(47,'DreamTown','Одежда','Эмблема','Расход',-700.00,'USD','Server card','2025-01-07'),(48,'Розетка','Скутер','Зарядка','Расход',-9000.00,'UAH','local card','2025-02-03'),(49,'DreamTown','Одежда','Шорты','Расход',-1000.00,'UAH','local card','2025-02-03'),(51,'DreamTown','Одежда','Шорты','Доход',600.00,'UAH','PC','2025-02-07'),(52,'DreamTown','Одежда','Шорты','Доход',500.00,'UAH','local card','2025-02-07'),(53,'Банки','ПриватБанк','Газ','Расход',-320.00,'EUR','japancard','2025-02-26'),(54,'DreamTown','Одежда','Эмблема','Расход',-100.00,'EUR','japancard','2025-02-26'),(55,'Банки','ПриватБанк','Вода','Расход',-2500.00,'UAH','local card','2025-02-26'),(56,'Розетка','Браслет','Бусины','Доход',150.00,'UAH','local card','2025-02-26'),(57,'DreamTown','Одежда','Футболка','Расход',-1500.00,'UAH','local card','2025-02-26');
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `type_pocket`
--

DROP TABLE IF EXISTS `type_pocket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `type_pocket` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `type_pocket`
--

LOCK TABLES `type_pocket` WRITE;
/*!40000 ALTER TABLE `type_pocket` DISABLE KEYS */;
/*!40000 ALTER TABLE `type_pocket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `gmail` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (12,'Vitaly','vitaly01@gmail.com','ed35d1c4595bd1ae6ec00a1beb87853243b7c6ce'),(13,'Vitaly ','vitaly02@gmail.com','0860b2f26999ef263892f6d9eaa3106ab48a9289');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-03 18:18:45
