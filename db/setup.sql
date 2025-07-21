-- ========================================================================
-- SCRIPT DE CRIAÇÃO DO BANCO DE DADOS "programacoes_filmes"
-- 
-- Este arquivo contém todos os comandos necessários para criar a estrutura
-- do banco de dados (tabelas, chaves primárias e estrangeiras) e popular 
-- com os dados iniciais utilizados na aplicação.
--
-- IMPORTANTE:
-- 1. Para executar este script, é necessário ter o MySQL instalado.
-- 2. A execução deve ser feita em um cliente MySQL, como o MySQL Workbench 
--    ou via terminal com o comando:
-- 
--      mysql -u SEU_USUARIO -p < setup.sql
--
-- 3. Esse script irá:
--    - Criar o banco de dados `programacoes_filmes` (se ainda não existir)
--    - Criar as tabelas: filme, canal, elenco, exibicao
--    - Inserir dados de exemplo em cada tabela
--
-- Dica: certifique-se de que o banco não existe previamente para evitar
-- conflitos, ou adapte os comandos conforme necessário.
-- ========================================================================


CREATE DATABASE  IF NOT EXISTS `programacoes_filmes` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `programacoes_filmes`;
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: programacoes_filmes
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

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
-- Table structure for table `canal`
--

DROP TABLE IF EXISTS `canal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `canal` (
  `num_canal` int(11) NOT NULL,
  `nome` varchar(50) NOT NULL,
  PRIMARY KEY (`num_canal`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `canal`
--

LOCK TABLES `canal` WRITE;
/*!40000 ALTER TABLE `canal` DISABLE KEYS */;
INSERT INTO `canal` VALUES (111,'AXN'),(222,'HBO'),(333,'Cinemax'),(444,'TNT');
/*!40000 ALTER TABLE `canal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elenco`
--

DROP TABLE IF EXISTS `elenco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `elenco` (
  `num_filme` int(11) NOT NULL,
  `nome_ator_atriz` varchar(100) NOT NULL,
  `protagonista` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`num_filme`,`nome_ator_atriz`),
  CONSTRAINT `elenco_ibfk_1` FOREIGN KEY (`num_filme`) REFERENCES `filme` (`num_filme`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elenco`
--

LOCK TABLES `elenco` WRITE;
/*!40000 ALTER TABLE `elenco` DISABLE KEYS */;
INSERT INTO `elenco` VALUES (90001,'Sam Worthington',1),(90001,'Sigourney Weaver',0),(90001,'Zoe Saldaña',1),(90002,'Kate Winslet',1),(90002,'Leonardo DiCaprio',1),(90003,'Carrie Fisher',1),(90003,'Harrison Ford',1),(90003,'Mark Hamill',1),(90004,'Chris Evans',1),(90004,'Josh Brolin',0),(90004,'Robert Downey Jr.',1),(90004,'Scarlett Johansson',1);
/*!40000 ALTER TABLE `elenco` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exibicao`
--

DROP TABLE IF EXISTS `exibicao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exibicao` (
  `num_filme` int(11) NOT NULL,
  `num_canal` int(11) NOT NULL,
  `data_exibicao` date NOT NULL,
  `hora_exibicao` time NOT NULL,
  PRIMARY KEY (`num_filme`,`num_canal`,`data_exibicao`,`hora_exibicao`),
  KEY `num_canal` (`num_canal`),
  CONSTRAINT `exibicao_ibfk_1` FOREIGN KEY (`num_filme`) REFERENCES `filme` (`num_filme`),
  CONSTRAINT `exibicao_ibfk_2` FOREIGN KEY (`num_canal`) REFERENCES `canal` (`num_canal`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exibicao`
--

LOCK TABLES `exibicao` WRITE;
/*!40000 ALTER TABLE `exibicao` DISABLE KEYS */;
INSERT INTO `exibicao` VALUES (90001,222,'2025-06-27','14:00:00'),(90002,333,'2025-06-28','09:30:00'),(90002,333,'2025-06-28','20:30:00'),(90003,111,'2025-06-27','19:45:00'),(90005,222,'2025-08-03','16:20:00'),(90005,333,'2025-08-03','16:20:00');
/*!40000 ALTER TABLE `exibicao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `filme`
--

DROP TABLE IF EXISTS `filme`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `filme` (
  `num_filme` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `ano` int(11) DEFAULT NULL,
  `duracao` int(11) DEFAULT NULL,
  PRIMARY KEY (`num_filme`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filme`
--

LOCK TABLES `filme` WRITE;
/*!40000 ALTER TABLE `filme` DISABLE KEYS */;
INSERT INTO `filme` VALUES (90001,'Avatar',2022,162),(90002,'Titanic',1997,194),(90003,'Star Wars',2019,NULL),(90004,'Vingadores Ultimato',2019,180),(90005,'Lilo & Stitch',2025,108);
/*!40000 ALTER TABLE `filme` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Trigger para validar que o ano de lançamento do filme não é futuro (INSERT)
DELIMITER $$
CREATE TRIGGER trg_validar_ano_filme_insert
BEFORE INSERT ON filme
FOR EACH ROW
BEGIN
    IF NEW.ano > YEAR(CURDATE()) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'O ano de lançamento do filme não pode ser futuro.';
    END IF;
END$$
DELIMITER ;

-- Trigger para validar que o ano de lançamento do filme não é futuro (UPDATE)
DELIMITER $$
CREATE TRIGGER trg_validar_ano_filme_update
BEFORE UPDATE ON filme
FOR EACH ROW
BEGIN
    IF NEW.ano > YEAR(CURDATE()) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'O ano de lançamento do filme não pode ser futuro.';
    END IF;
END$$
DELIMITER ;


-- Dump completed on 2025-07-11 21:42:17