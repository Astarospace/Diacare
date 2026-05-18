-- MySQL dump 10.13  Distrib 8.4.9, for Linux (x86_64)
--
-- Host: localhost    Database: Diacare
-- ------------------------------------------------------
-- Server version	8.4.9

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
-- Table structure for table `AdminUsers`
--

DROP TABLE IF EXISTS `AdminUsers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `AdminUsers` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `FullName` varchar(120) NOT NULL,
  `PhoneNumber` varchar(20) NOT NULL,
  `PasswordHash` varchar(255) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `AdminUsers`
--

LOCK TABLES `AdminUsers` WRITE;
/*!40000 ALTER TABLE `AdminUsers` DISABLE KEYS */;
INSERT INTO `AdminUsers` VALUES (1,'Admin','01000000000','1234');
/*!40000 ALTER TABLE `AdminUsers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Appointments`
--

DROP TABLE IF EXISTS `Appointments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Appointments` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `PatientId` int NOT NULL,
  `DoctorId` int NOT NULL,
  `ScheduleId` int NOT NULL,
  `Status` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`Id`),
  KEY `PatientId` (`PatientId`),
  KEY `DoctorId` (`DoctorId`),
  KEY `ScheduleId` (`ScheduleId`),
  CONSTRAINT `Appointments_ibfk_1` FOREIGN KEY (`PatientId`) REFERENCES `Patients` (`Id`) ON DELETE CASCADE,
  CONSTRAINT `Appointments_ibfk_2` FOREIGN KEY (`DoctorId`) REFERENCES `Doctors` (`Id`) ON DELETE CASCADE,
  CONSTRAINT `Appointments_ibfk_3` FOREIGN KEY (`ScheduleId`) REFERENCES `Schedules` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Appointments`
--

LOCK TABLES `Appointments` WRITE;
/*!40000 ALTER TABLE `Appointments` DISABLE KEYS */;
INSERT INTO `Appointments` VALUES (21,12,6,17,4),(22,12,6,16,3);
/*!40000 ALTER TABLE `Appointments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DoctorReviews`
--

DROP TABLE IF EXISTS `DoctorReviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `DoctorReviews` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `DoctorId` int NOT NULL,
  `PatientId` int NOT NULL,
  `Rating` int NOT NULL,
  `Comment` varchar(1000) DEFAULT '',
  `CreatedAt` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Id`),
  KEY `DoctorId` (`DoctorId`),
  KEY `PatientId` (`PatientId`),
  CONSTRAINT `DoctorReviews_ibfk_1` FOREIGN KEY (`DoctorId`) REFERENCES `Doctors` (`Id`) ON DELETE CASCADE,
  CONSTRAINT `DoctorReviews_ibfk_2` FOREIGN KEY (`PatientId`) REFERENCES `Patients` (`Id`) ON DELETE CASCADE,
  CONSTRAINT `CHK_Review_Rating` CHECK (((`Rating` >= 1) and (`Rating` <= 5)))
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DoctorReviews`
--

LOCK TABLES `DoctorReviews` WRITE;
/*!40000 ALTER TABLE `DoctorReviews` DISABLE KEYS */;
INSERT INTO `DoctorReviews` VALUES (1,1,1,5,'Excellent doctor, very knowledgeable.','2026-05-09 15:11:18'),(2,1,2,4,'Good but had to wait a bit.','2026-05-09 15:11:18'),(3,1,3,5,'Life-changing care!','2026-05-09 15:11:18'),(4,1,4,3,'Okay, but communication could improve.','2026-05-09 15:11:18'),(5,1,5,5,'Best diabetes specialist I have met.','2026-05-09 15:11:18'),(6,1,6,4,'Very thorough explanation.','2026-05-09 15:11:18'),(7,1,7,2,'Seemed rushed.','2026-05-09 15:11:18'),(8,1,8,5,'Highly recommend.','2026-05-09 15:11:18'),(9,1,9,4,'Professional and friendly.','2026-05-09 15:11:18'),(10,1,10,5,'Great follow-up care.','2026-05-09 15:11:18'),(11,2,1,4,'Good cardiologist.','2026-05-09 15:11:18'),(12,2,2,5,'Saved my father’s life.','2026-05-09 15:11:18'),(13,2,3,4,'Clear advice on lifestyle changes.','2026-05-09 15:11:18'),(14,2,4,5,'Long wait for appointment.','2026-05-09 15:11:18'),(15,2,5,5,'Very compassionate.','2026-05-09 15:11:18'),(16,2,6,4,'Explained everything well.','2026-05-09 15:11:18'),(17,2,7,4,'Solid doctor.','2026-05-09 15:11:18'),(18,2,8,5,'Would visit again.','2026-05-09 15:11:18'),(19,2,9,3,'Seemed a bit distracted.','2026-05-09 15:11:18'),(20,3,1,5,'Amazing endocrinologist.','2026-05-09 15:11:18'),(21,3,2,4,'Very patient with questions.','2026-05-09 15:11:18'),(22,3,3,5,'Finally got my hormones balanced.','2026-05-09 15:11:18'),(23,3,4,3,'Wait time was long.','2026-05-09 15:11:18'),(24,3,5,4,'Good follow-up plan.','2026-05-09 15:11:18'),(25,3,6,5,'Very knowledgeable.','2026-05-09 15:11:18'),(26,3,7,4,'Friendly staff as well.','2026-05-09 15:11:18'),(27,3,8,5,'Highly recommended.','2026-05-09 15:11:18'),(28,3,9,2,'Did not listen to all symptoms.','2026-05-09 15:11:18'),(29,4,1,5,'Wonderful with children.','2026-05-09 15:11:18'),(30,4,2,5,'My kids love her.','2026-05-09 15:11:18'),(31,4,3,4,'Good but clinic was busy.','2026-05-09 15:11:18'),(32,4,4,3,'Average experience.','2026-05-09 15:11:18'),(33,4,5,5,'Very gentle.','2026-05-09 15:11:18'),(34,4,6,4,'Answered all my concerns.','2026-05-09 15:11:18'),(35,4,7,5,'Best pediatrician around.','2026-05-09 15:11:18'),(36,4,8,4,'Quick visit, but effective.','2026-05-09 15:11:18'),(37,4,9,5,'Takes time to explain.','2026-05-09 15:11:18'),(38,4,10,3,'Felt a bit rushed.','2026-05-09 15:11:18'),(39,5,1,5,'Excellent diabetes care.','2026-05-09 15:11:18'),(40,5,2,4,'Good but hard to get appointment.','2026-05-09 15:11:18'),(41,5,3,5,'Very understanding.','2026-05-09 15:11:18'),(42,5,4,5,'Provided great diet plan.','2026-05-09 15:11:18'),(43,5,5,3,'Okay, nothing special.','2026-05-09 15:11:18'),(44,5,6,4,'Pleasant manner.','2026-05-09 15:11:18'),(45,5,7,5,'Would recommend to family.','2026-05-09 15:11:18'),(46,5,8,4,'Solid advice.','2026-05-09 15:11:18'),(48,6,12,3,'Bad Doctor','2026-05-16 19:28:31'),(49,6,12,5,'Good Doctor','2026-05-16 19:28:41'),(50,6,12,5,'Test','2026-05-16 22:59:22'),(51,6,12,2,'Test','2026-05-16 23:01:58');
/*!40000 ALTER TABLE `DoctorReviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Doctors`
--

DROP TABLE IF EXISTS `Doctors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Doctors` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `FullName` varchar(120) NOT NULL,
  `PhoneNumber` varchar(20) NOT NULL,
  `PasswordHash` varchar(255) NOT NULL,
  `Specialty` varchar(80) NOT NULL DEFAULT 'Diabetes Specialist',
  `RatingSum` int NOT NULL DEFAULT '0',
  `RatingCount` int NOT NULL DEFAULT '0',
  `ImagePath` varchar(255) DEFAULT '/images/doctor-placeholder.svg',
  PRIMARY KEY (`Id`),
  CONSTRAINT `CHK_Doctor_RatingCount` CHECK ((`RatingCount` >= 0)),
  CONSTRAINT `CHK_Doctor_RatingSum` CHECK ((`RatingSum` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Doctors`
--

LOCK TABLES `Doctors` WRITE;
/*!40000 ALTER TABLE `Doctors` DISABLE KEYS */;
INSERT INTO `Doctors` VALUES (1,'Dr. Sarah Osama','01026310118','1234','Diabetes Specialist',46,11,'/static/images/doctor1.png'),(2,'Dr. Michael Maged','01046012083','1234','Cardiologist',39,9,'/static/images/doctor2.png'),(3,'Dr. Gad Ahmed','01094332708','1234','Endocrinologist',37,9,'/static/images/doctor3.png'),(4,'Dr. Mahmoud Gaber','01072794661','1234','Pediatrician',43,10,'/static/images/doctor4.png'),(5,'Dr. Maria Ayman','01097753886','1234','Diabetes Specialist',35,8,'/static/images/doctor5.png'),(6,'Dr. Samy','01000000001','1234','Software Engineering',15,4,'/static/images/doctor2.png');
/*!40000 ALTER TABLE `Doctors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Patients`
--

DROP TABLE IF EXISTS `Patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Patients` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `FullName` varchar(120) NOT NULL,
  `PhoneNumber` varchar(20) NOT NULL,
  `PasswordHash` varchar(255) NOT NULL,
  `Age` int NOT NULL,
  `Gender` int NOT NULL,
  PRIMARY KEY (`Id`),
  CONSTRAINT `CHK_Patient_Age` CHECK (((`Age` >= 1) and (`Age` <= 120)))
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Patients`
--

LOCK TABLES `Patients` WRITE;
/*!40000 ALTER TABLE `Patients` DISABLE KEYS */;
INSERT INTO `Patients` VALUES (1,'Aliaa Ahmed','01064225676','1234',28,2),(2,'Omar Khaled','01085961132','1234',34,1),(3,'Mary Ashraf','01004261254','1234',45,2),(4,'Khaled Ali','01043531808','1234',22,1),(5,'Wageeh Shady','01043790568','1234',30,1),(6,'Samir Abdallah','01034540768','1234',55,1),(7,'Ghada Samir','01002560461','1234',60,2),(8,'Amir Yasir','01081702486','1234',27,1),(9,'Mai Bakr','01057392574','1234',32,2),(10,'Barakat Abulkheir','01047764245','1234',41,1),(12,'Mina Hesham Makeen','01111111111','1234',24,1);
/*!40000 ALTER TABLE `Patients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Schedules`
--

DROP TABLE IF EXISTS `Schedules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Schedules` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `DoctorId` int NOT NULL,
  `Hours` varchar(80) NOT NULL,
  `Status` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`Id`),
  KEY `DoctorId` (`DoctorId`),
  CONSTRAINT `Schedules_ibfk_1` FOREIGN KEY (`DoctorId`) REFERENCES `Doctors` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Schedules`
--

LOCK TABLES `Schedules` WRITE;
/*!40000 ALTER TABLE `Schedules` DISABLE KEYS */;
INSERT INTO `Schedules` VALUES (1,1,'04:00-06:00 | Saturday',1),(2,1,'06:00-08:00 | Saturday',1),(3,1,'08:00-10:00 | Saturday',1),(4,2,'04:00-06:00 | Saturday',1),(5,2,'06:00-08:00 | Saturday',1),(6,2,'08:00-10:00 | Saturday',1),(7,3,'04:00-06:00 | Saturday',1),(8,3,'06:00-08:00 | Saturday',1),(9,3,'08:00-10:00 | Saturday',1),(10,4,'04:00-06:00 | Saturday',1),(11,4,'06:00-08:00 | Saturday',1),(12,4,'08:00-10:00 | Saturday',1),(13,5,'04:00-06:00 | Saturday',1),(14,5,'06:00-08:00 | Saturday',1),(15,5,'08:00-10:00 | Saturday',1),(16,6,'04:00-06:00 | Saturday',1),(17,6,'06:00-08:00 | Saturday',1),(18,6,'08:00-10:00 | Saturday',1);
/*!40000 ALTER TABLE `Schedules` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-16 23:08:11
