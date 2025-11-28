-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 172.27.0.50    Database: grp05ClinPasteur
-- ------------------------------------------------------
-- Server version	5.5.5-10.11.11-MariaDB-0+deb12u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Chirurgiens`
--

DROP TABLE IF EXISTS `Chirurgiens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Chirurgiens` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idRoles` int(11) NOT NULL,
  `idPersonnel` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_chir_roles` (`idRoles`),
  KEY `fk_chir_personnel` (`idPersonnel`),
  CONSTRAINT `fk_chir_personnel` FOREIGN KEY (`idPersonnel`) REFERENCES `Personnel` (`id`),
  CONSTRAINT `fk_chir_roles` FOREIGN KEY (`idRoles`) REFERENCES `Roles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Chirurgiens`
--

LOCK TABLES `Chirurgiens` WRITE;
/*!40000 ALTER TABLE `Chirurgiens` DISABLE KEYS */;
/*!40000 ALTER TABLE `Chirurgiens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DetailEtude`
--

DROP TABLE IF EXISTS `DetailEtude`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `DetailEtude` (
  `idPatient` int(11) NOT NULL,
  `idEtude` int(11) NOT NULL,
  `idEtatInclusion` int(11) DEFAULT NULL,
  `dateInclusion` date DEFAULT NULL,
  `idMaladie` int(11) DEFAULT NULL,
  PRIMARY KEY (`idPatient`,`idEtude`),
  KEY `fk_detet_etude` (`idEtude`),
  KEY `fk_detet_etat` (`idEtatInclusion`),
  KEY `fk_detailEtude_maladie` (`idMaladie`),
  CONSTRAINT `fk_detailEtude_maladie` FOREIGN KEY (`idMaladie`) REFERENCES `Maladies` (`id`),
  CONSTRAINT `fk_detet_etat` FOREIGN KEY (`idEtatInclusion`) REFERENCES `EtatInclusion` (`id`),
  CONSTRAINT `fk_detet_etude` FOREIGN KEY (`idEtude`) REFERENCES `Etudes` (`id`),
  CONSTRAINT `fk_detet_patient` FOREIGN KEY (`idPatient`) REFERENCES `Patients` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DetailEtude`
--

LOCK TABLES `DetailEtude` WRITE;
/*!40000 ALTER TABLE `DetailEtude` DISABLE KEYS */;
INSERT INTO `DetailEtude` VALUES (2,1,2,'2020-03-01',NULL),(2,2,1,'2025-11-23',1),(4,3,1,'2022-08-01',NULL),(4,4,1,'2023-02-01',NULL),(5,4,1,'2023-04-01',NULL),(6,4,2,'2023-06-15',NULL),(7,5,1,'2021-03-20',NULL),(8,1,2,'2025-11-23',5);
/*!40000 ALTER TABLE `DetailEtude` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EtatInclusion`
--

DROP TABLE IF EXISTS `EtatInclusion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `EtatInclusion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `libelleEtat` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EtatInclusion`
--

LOCK TABLES `EtatInclusion` WRITE;
/*!40000 ALTER TABLE `EtatInclusion` DISABLE KEYS */;
INSERT INTO `EtatInclusion` VALUES (1,'Inclus'),(2,'En cours'),(3,'Terminé'),(4,'Exclu');
/*!40000 ALTER TABLE `EtatInclusion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Etudes`
--

DROP TABLE IF EXISTS `Etudes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Etudes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nomEtu` varchar(100) NOT NULL,
  `descEtude` text DEFAULT NULL,
  `idTypeEtude` int(11) DEFAULT NULL,
  `idOrganisme` int(11) DEFAULT NULL,
  `dateDebEtu` date DEFAULT NULL,
  `dateFinEtu` date DEFAULT NULL,
  `idMedResponsable` int(11) DEFAULT NULL,
  `idProtocole` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_etudes_type` (`idTypeEtude`),
  KEY `fk_etudes_organisme` (`idOrganisme`),
  KEY `fk_etudes_med` (`idMedResponsable`),
  KEY `fk_etudes_proto` (`idProtocole`),
  CONSTRAINT `fk_etudes_med` FOREIGN KEY (`idMedResponsable`) REFERENCES `Personnel` (`id`),
  CONSTRAINT `fk_etudes_organisme` FOREIGN KEY (`idOrganisme`) REFERENCES `Organismes` (`id`),
  CONSTRAINT `fk_etudes_proto` FOREIGN KEY (`idProtocole`) REFERENCES `Protocole` (`id`),
  CONSTRAINT `fk_etudes_type` FOREIGN KEY (`idTypeEtude`) REFERENCES `TypeEtudes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Etudes`
--

LOCK TABLES `Etudes` WRITE;
/*!40000 ALTER TABLE `Etudes` DISABLE KEYS */;
INSERT INTO `Etudes` VALUES (1,'Étude Cancer Poumon 2020','Suivi de patients atteints de cancer du poumon',2,1,'2020-01-01','2024-12-31',1,NULL),(2,'Étude Cirrhose Lyon','Ancien essai (non utilisé car hors cancer, conservé pour cohérence historique)',1,2,'2019-05-15','2023-12-31',2,NULL),(3,'Essai Chirurgie Cancer Rectum','Évaluation des résultats post-opératoires en chirurgie rectum',2,1,'2022-01-01','2026-12-31',4,NULL),(4,'Protocole RecaRe','Essai multicentrique sur la prise en charge du cancer rectum : chirurgie + radiochimiothérapie',2,2,'2023-01-01','2027-12-31',4,NULL),(5,'Étude Cancer Sein','Essai clinique sur traitements innovants cancer du sein',2,3,'2021-01-01','2025-12-31',5,NULL),(6,'Test','Test',NULL,NULL,NULL,NULL,6,NULL),(7,'TEST2','TEST2',1,NULL,NULL,NULL,NULL,NULL),(8,'TEST3','TEST3',1,1,'2025-11-22','2025-11-22',NULL,NULL),(9,'test4','test4',1,1,'2025-11-22','2025-11-22',2,NULL),(10,'test5','test5',1,1,'2025-11-22','2025-11-22',2,2),(11,'test6','test6',1,1,'2025-11-22','2025-11-22',3,1),(12,'test7','test7',1,1,'2025-11-22','2025-11-05',2,1),(13,'Etude Cancer Foie','Essai clinique sur traitements innovants cancer du foie',1,1,'2025-11-23','2025-11-23',2,1),(14,'Etude Cancer Foie 2','Essai clinique sur traitements innovants cancer du foie',1,1,'2025-11-28','2025-11-23',2,1),(15,'Etude test','Test',1,1,'2025-11-28','2025-11-28',2,1);
/*!40000 ALTER TABLE `Etudes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Maladies`
--

DROP TABLE IF EXISTS `Maladies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Maladies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nomMaladie` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Maladies`
--

LOCK TABLES `Maladies` WRITE;
/*!40000 ALTER TABLE `Maladies` DISABLE KEYS */;
INSERT INTO `Maladies` VALUES (1,'Cancer du poumon'),(2,'Cancer du foie'),(3,'Cancer du rectum'),(4,'Cancer du rein'),(5,'Cancer du sein');
/*!40000 ALTER TABLE `Maladies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Organes`
--

DROP TABLE IF EXISTS `Organes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Organes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nomOrgane` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Organes`
--

LOCK TABLES `Organes` WRITE;
/*!40000 ALTER TABLE `Organes` DISABLE KEYS */;
INSERT INTO `Organes` VALUES (1,'Poumon'),(2,'Foie'),(3,'Rectum'),(4,'Rein'),(5,'Sein');
/*!40000 ALTER TABLE `Organes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Organismes`
--

DROP TABLE IF EXISTS `Organismes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Organismes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nomOrg` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Organismes`
--

LOCK TABLES `Organismes` WRITE;
/*!40000 ALTER TABLE `Organismes` DISABLE KEYS */;
INSERT INTO `Organismes` VALUES (1,'Institut Pasteur'),(2,'CHU Lyon'),(3,'INSERM');
/*!40000 ALTER TABLE `Organismes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Patients`
--

DROP TABLE IF EXISTS `Patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Patients` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nomPat` varchar(100) DEFAULT NULL,
  `prenomPat` varchar(100) DEFAULT NULL,
  `dateNaisPat` date DEFAULT NULL,
  `sexe` char(1) DEFAULT NULL,
  `numDossierClinique` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numDossierClinique` (`numDossierClinique`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Patients`
--

LOCK TABLES `Patients` WRITE;
/*!40000 ALTER TABLE `Patients` DISABLE KEYS */;
INSERT INTO `Patients` VALUES (2,'Dupont','Jean','1970-05-12','M','DCL-0001'),(3,'Martin','Claire','1982-08-23','F','DCL-0002'),(4,'Lopez','Maria','1965-11-03','F','DCL-0003'),(5,'Rousseau','Camille','1975-09-14','F','DCL-0004'),(6,'Petit','Nicolas','1980-02-25','M','DCL-0005'),(7,'Fabre','Elise','1968-07-09','F','DCL-0006'),(8,'Durand','Sophie','1977-04-19','F','DCL-0007'),(9,'rrr','yyyy','2022-02-02','F','dd-030'),(10,'Test1','Test1','2025-11-22','F','Test1');
/*!40000 ALTER TABLE `Patients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Patients_Maladies`
--

DROP TABLE IF EXISTS `Patients_Maladies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Patients_Maladies` (
  `idPatient` int(11) NOT NULL,
  `idMaladie` int(11) NOT NULL,
  `idOrganes` int(11) DEFAULT NULL,
  `idStade` int(11) DEFAULT NULL,
  `dateDiagnostic` date NOT NULL,
  PRIMARY KEY (`idPatient`,`idMaladie`,`dateDiagnostic`),
  KEY `fk_pm_maladie` (`idMaladie`),
  KEY `fk_pm_organe` (`idOrganes`),
  KEY `fk_pm_stade` (`idStade`),
  CONSTRAINT `fk_pm_maladie` FOREIGN KEY (`idMaladie`) REFERENCES `Maladies` (`id`),
  CONSTRAINT `fk_pm_organe` FOREIGN KEY (`idOrganes`) REFERENCES `Organes` (`id`),
  CONSTRAINT `fk_pm_patient` FOREIGN KEY (`idPatient`) REFERENCES `Patients` (`id`),
  CONSTRAINT `fk_pm_stade` FOREIGN KEY (`idStade`) REFERENCES `Stades` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Patients_Maladies`
--

LOCK TABLES `Patients_Maladies` WRITE;
/*!40000 ALTER TABLE `Patients_Maladies` DISABLE KEYS */;
INSERT INTO `Patients_Maladies` VALUES (2,1,1,2,'0000-00-00'),(3,2,2,3,'0000-00-00'),(4,4,4,4,'0000-00-00'),(5,3,3,2,'0000-00-00'),(6,3,3,3,'0000-00-00'),(7,3,3,2,'0000-00-00'),(8,5,5,1,'0000-00-00');
/*!40000 ALTER TABLE `Patients_Maladies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Personnel`
--

DROP TABLE IF EXISTS `Personnel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Personnel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nomSoignant` varchar(100) DEFAULT NULL,
  `prenomSoignant` varchar(100) DEFAULT NULL,
  `idSpecialite` int(11) DEFAULT NULL,
  `idService` int(11) DEFAULT NULL,
  `idRole` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_personnel_spec` (`idSpecialite`),
  KEY `fk_personnel_serv` (`idService`),
  KEY `fk_personnel_role` (`idRole`),
  CONSTRAINT `fk_personnel_role` FOREIGN KEY (`idRole`) REFERENCES `Roles` (`id`),
  CONSTRAINT `fk_personnel_serv` FOREIGN KEY (`idService`) REFERENCES `Services` (`id`),
  CONSTRAINT `fk_personnel_spec` FOREIGN KEY (`idSpecialite`) REFERENCES `Specialites` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Personnel`
--

LOCK TABLES `Personnel` WRITE;
/*!40000 ALTER TABLE `Personnel` DISABLE KEYS */;
INSERT INTO `Personnel` VALUES (1,'Durand','Paul',1,1,1),(2,'Bernard','Sophie',2,2,2),(3,'Garcia','Elena',3,3,2),(4,'Lefevre','Antoine',4,4,4),(5,'Marchand','Isabelle',5,5,5),(6,'essai','Us02',NULL,NULL,NULL);
/*!40000 ALTER TABLE `Personnel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Protocole`
--

DROP TABLE IF EXISTS `Protocole`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Protocole` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `libelleProtocole` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Protocole`
--

LOCK TABLES `Protocole` WRITE;
/*!40000 ALTER TABLE `Protocole` DISABLE KEYS */;
INSERT INTO `Protocole` VALUES (1,'Protocole A'),(2,'Protocole B'),(3,'Protocole C');
/*!40000 ALTER TABLE `Protocole` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Questionnaire`
--

DROP TABLE IF EXISTS `Questionnaire`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Questionnaire` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Questionnaire`
--

LOCK TABLES `Questionnaire` WRITE;
/*!40000 ALTER TABLE `Questionnaire` DISABLE KEYS */;
/*!40000 ALTER TABLE `Questionnaire` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Roles`
--

DROP TABLE IF EXISTS `Roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `libelleRole` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Roles`
--

LOCK TABLES `Roles` WRITE;
/*!40000 ALTER TABLE `Roles` DISABLE KEYS */;
INSERT INTO `Roles` VALUES (1,'Chef de service'),(2,'Médecin référent'),(3,'Attaché de recherche clinique'),(4,'Chirurgien digestif'),(5,'Oncologue mammaire');
/*!40000 ALTER TABLE `Roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Services`
--

DROP TABLE IF EXISTS `Services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Services` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `libelleServ` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Services`
--

LOCK TABLES `Services` WRITE;
/*!40000 ALTER TABLE `Services` DISABLE KEYS */;
INSERT INTO `Services` VALUES (1,'Service Oncologie'),(2,'Service Hépato'),(3,'Service Néphrologie'),(4,'Service Chirurgie Digestive'),(5,'Service Sénologie');
/*!40000 ALTER TABLE `Services` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Specialites`
--

DROP TABLE IF EXISTS `Specialites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Specialites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `libelleSpec` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Specialites`
--

LOCK TABLES `Specialites` WRITE;
/*!40000 ALTER TABLE `Specialites` DISABLE KEYS */;
INSERT INTO `Specialites` VALUES (1,'Oncologie'),(2,'Hépato-gastroentérologie'),(3,'Néphrologie'),(4,'Chirurgie digestive'),(5,'Oncologie mammaire');
/*!40000 ALTER TABLE `Specialites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Stades`
--

DROP TABLE IF EXISTS `Stades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Stades` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nomStade` varchar(5) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Stades`
--

LOCK TABLES `Stades` WRITE;
/*!40000 ALTER TABLE `Stades` DISABLE KEYS */;
INSERT INTO `Stades` VALUES (1,'I'),(2,'II'),(3,'III'),(4,'IV');
/*!40000 ALTER TABLE `Stades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TypeEtudes`
--

DROP TABLE IF EXISTS `TypeEtudes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `TypeEtudes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `libelleEtu` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TypeEtudes`
--

LOCK TABLES `TypeEtudes` WRITE;
/*!40000 ALTER TABLE `TypeEtudes` DISABLE KEYS */;
INSERT INTO `TypeEtudes` VALUES (1,'Étude observationnelle'),(2,'Essai clinique randomisé'),(3,'Étude prospective');
/*!40000 ALTER TABLE `TypeEtudes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Utilisateurs`
--

DROP TABLE IF EXISTS `Utilisateurs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Utilisateurs` (
  `identifiant` int(11) NOT NULL AUTO_INCREMENT,
  `nomUtilisateur` varchar(100) NOT NULL,
  `motDePasse` varchar(255) NOT NULL,
  PRIMARY KEY (`identifiant`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Utilisateurs`
--

LOCK TABLES `Utilisateurs` WRITE;
/*!40000 ALTER TABLE `Utilisateurs` DISABLE KEYS */;
INSERT INTO `Utilisateurs` VALUES (1,'Emilie','Emilie12345%'),(3,'Poisson','Poisson12345%');
/*!40000 ALTER TABLE `Utilisateurs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'grp05ClinPasteur'
--

--
-- Dumping routines for database 'grp05ClinPasteur'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-28 22:10:10
