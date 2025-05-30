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
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (2,'Планшет',3,13),(3,'Телефон',4,13),(5,'Повербанк',4,13),(6,'Одежда',5,13),(9,'Скутер',4,13),(10,'Браслет',4,13),(11,'Окорочка',6,13),(12,'Молоко',6,13),(14,'ПриватБанк',8,13),(15,'Монобанк',8,13),(16,'Ощадбанк',8,13),(17,'Райффайзен Банк',8,13),(34,'Eat',16,15),(35,'Продукти',17,16),(36,'Рітейл / Продукти',18,16),(41,'Фармацевтика / Медицина',23,16),(42,'Фармацевтика / Медицина',22,16),(43,'Будівництво / Матеріали',19,16),(44,'ІТ / Послуги',25,16),(45,'Єлектроніка',26,16),(46,'Переферія',26,16),(47,'Запчастини',26,16),(48,'АТБ',27,17),(49,'Фора',27,17),(50,'Варус',27,17);
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
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `counterparties`
--

LOCK TABLES `counterparties` WRITE;
/*!40000 ALTER TABLE `counterparties` DISABLE KEYS */;
INSERT INTO `counterparties` VALUES (3,'Фокстрот',13),(4,'Розетка',13),(5,'DreamTown',13),(6,'Varus',13),(8,'Банк',13),(16,'Glovo',15),(17,'АТБ-Маркет',16),(18,'Procter & Gamble Україна',16),(19,'Епіцентр К',16),(22,'Дарниця',16),(23,'Аптека АНЦ',16),(25,'DeNovo',16),(26,'Happy-pc',16),(27,'Магазини',17);
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
  `status` tinyint(1) DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pocket`
--

LOCK TABLES `pocket` WRITE;
/*!40000 ALTER TABLE `pocket` DISABLE KEYS */;
INSERT INTO `pocket` VALUES (2,'privatcard','debit','EUR','2030-12-31 00:00:00',NULL,130643.00,'#e35e78',NULL,1,13),(3,'japancard','debit','EUR','2024-12-06 00:00:00',NULL,27478.00,NULL,'C://Finans_programm/images/background_card\\cat.png',NULL,13),(4,'local card','kredit','UAH','2035-12-31 00:00:00',NULL,-41340.00,NULL,'C://Finans_programm/images/background_card\\LOGO_2.png',1,13),(5,'PC','debit','UAH','2021-06-07 00:00:00',NULL,29985754.33,'#ff0000',NULL,NULL,13),(6,'visaUSD','debit','USD','2004-04-25 00:00:00',NULL,-42225.00,NULL,'C://Finans_programm/images/background_card\\logo_py.png',NULL,13),(9,'Server card','debit','USD','2011-01-13 00:00:00',NULL,56090.00,'#fbff42',NULL,NULL,13),(10,'Maincard','debit','UAH','2004-04-25 00:00:00',NULL,10000.00,'#ff00ff',NULL,NULL,13),(12,'Card for cars','debit','EUR','2026-04-25 00:00:00','2025-05-02 17:29:46',10000.00,NULL,'C://Finans_programm/images/background_card\\nier.jfif',1,13),(16,'ABIBA','debit','UAH','2025-04-11 00:00:00',NULL,-13889.00,'#b68b8b',NULL,NULL,13),(18,'TC','Debit','UAH','2025-04-25 00:00:00',NULL,15000.00,'#ff4246',NULL,NULL,14),(21,'Ira','Debit','EUR','2025-05-21 00:00:00',NULL,101100.00,'#fc238a',NULL,NULL,13),(22,'Defolt','Debit','EUR','2025-05-30 00:00:00',NULL,9700.00,'#918bb6',NULL,NULL,15),(23,'Universal','Debit','USD','2025-05-30 00:00:00',NULL,7396.00,'#ca7777',NULL,NULL,16),(24,'Privat Universal','Debit','UAH','2004-04-25 00:00:00',NULL,5555.00,NULL,'C://Finans_programm/images/background_card\\nier.jfif',NULL,16),(25,'Universal','Debit','UAH','2030-05-31 00:00:00',NULL,50000.00,NULL,'C://Finans_programm/images/background_card\\cat.png',1,17),(26,'Mains for cars','Debit','UAH','2027-05-20 00:00:00','2025-05-28 22:21:11',9600.00,NULL,'C://Finans_programm/images/background_card\\nier.jfif',1,17),(29,'B','Debit','EUR','2025-05-30 00:00:00','2025-05-28 23:29:04',-130.00,'#f99999',NULL,NULL,17),(30,'B2','Debit','UAH','2025-05-22 00:00:00',NULL,212.00,'#c77aa5',NULL,NULL,17);
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
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subcategory`
--

LOCK TABLES `subcategory` WRITE;
/*!40000 ALTER TABLE `subcategory` DISABLE KEYS */;
INSERT INTO `subcategory` VALUES (1,'Процессор',2,13),(2,'Зарядка',9,13),(3,'Бусины',10,13),(4,'Футболка',6,13),(5,'Шорты',6,13),(6,'Эмблема',6,13),(7,'Электроэнергия',14,13),(8,'Газ',14,13),(9,'Вода',14,13),(10,'Интернет',14,13),(11,'Аккамулятор',5,13),(32,'Pizza',34,15),(33,'KFC',34,15),(34,'MacDonalds',34,15),(35,'Продуктові мережі',35,16),(36,'Побутова хімія\n\n',36,16),(41,'Ліки',41,16),(42,'Виробники ліків',42,16),(43,'Будівельні супермаркети',43,16),(44,'Хмарні сервіси',44,16),(45,'Відеокарта',47,16),(46,'Процесор',47,16),(47,'Опреративна пам\'ять',47,16),(48,'Термопаста',46,16),(49,'Навушники',45,16),(51,'Морозиво',48,17),(52,'Риба',50,17),(53,'Напої',49,17);
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
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=112 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (96,'АТБ-Маркет','Продукти','Продуктові мережі','Витрата',-100.00,'USD','Universal','2025-05-09',16),(97,'Епіцентр К','Будівництво / Матеріали','Будівельні супермаркети','Витрата',-450.00,'USD','Universal','2025-05-17',16),(98,'Аптека АНЦ','Фармацевтика / Медицина','Ліки','Витрата',-55.00,'USD','Universal','2025-05-21',16),(99,'DeNovo','ІТ / Послуги','Хмарні сервіси','Дохід',350.00,'USD','Universal','2025-05-01',16),(100,'Дарниця','Фармацевтика / Медицина','Виробники ліків','Дохід',700.00,'USD','Universal','2025-05-02',16),(101,'Happy-pc','Єлектроніка','Навушники','Витрата',-999.00,'USD','Universal','2025-05-28',16),(102,'Happy-pc','Запчастини','Відеокарта','Витрата',-1500.00,'USD','Universal','2024-05-22',16),(103,'Happy-pc','Запчастини','Опреративна пам\'ять','Витрата',-550.00,'USD','Universal','2025-01-27',16),(105,'Магазини','Фора','Напої','Витрата',-500.00,'USD','Mains for cars','2025-05-05',17),(106,'Магазини','АТБ','Морозиво','Дохід',100.00,'USD','Mains for cars','2025-05-30',17),(110,'Магазини','Фора','Напої','Витрата',-100.00,'UAH','B2','2025-05-28',17),(111,'Магазини','Фора','Напої','Витрата',-200.00,'EUR','B','2025-05-28',17);
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
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (12,'Vitaly','vitaly01@gmail.com','ed35d1c4595bd1ae6ec00a1beb87853243b7c6ce'),(13,'Vitaly ','vitaly02@gmail.com','0860b2f26999ef263892f6d9eaa3106ab48a9289'),(14,'Vitaly','vital@gmail.com','d57483241b6081adfde21e99348291ea0ac90049'),(15,'Gregor','gregor@gmail.com','779f6618b4a4c343a154c5e26bb842e4481dd938'),(16,'Andry','Andry@gmail.com','bace61870e44978aef5992b3ee0bb343dada4a68'),(17,'Nady','Nady@gmail.com','3586838fc465c3a4ef815eb7cfd6299d464a55fd'),(20,'Vita','Vita@gmail.com','34b31896c29790716802793186af6a0695f72f12');
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

-- Dump completed on 2025-05-30 17:32:01
