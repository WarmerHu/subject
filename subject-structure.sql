-- MySQL dump 10.13  Distrib 5.6.28, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: subject
-- ------------------------------------------------------
-- Server version	5.6.28-0ubuntu0.15.04.1

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

--database
--create database subject default character set utf8 collate utf8_general_ci;

--
-- Table structure for table `activity`
--

DROP TABLE IF EXISTS `activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `activity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userId` int(11) NOT NULL,
  `content` varchar(255) NOT NULL,
  `time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `activity_userId` (`userId`),
  CONSTRAINT `activity_userId` FOREIGN KEY (`userId`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=493 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `collection`
--

DROP TABLE IF EXISTS `collection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `collection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exerciseId` int(11) NOT NULL,
  `userId` int(11) NOT NULL,
  `note` text,
  `rightTime` int(11) DEFAULT '0',
  `wrongTime` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `subject_exerciseId` (`exerciseId`),
  KEY `subject_userId` (`userId`),
  CONSTRAINT `subject_exerciseId` FOREIGN KEY (`exerciseId`) REFERENCES `exercise` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `subject_userId` FOREIGN KEY (`userId`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `complaint`
--

DROP TABLE IF EXISTS `complaint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `complaint` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userId` int(11) DEFAULT NULL,
  `titleId` int(11) DEFAULT NULL,
  `content` text,
  `authorid` int(11) DEFAULT NULL,
  `state` enum('NORMAL','CANCEL') DEFAULT NULL,
  `topicid` int(11) DEFAULT NULL,
  `opinionid` int(11) DEFAULT NULL,
  `resourceid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `userId` (`userId`),
  KEY `titleId` (`titleId`),
  KEY `fk_author_user` (`authorid`),
  KEY `fk_topicid_com` (`topicid`),
  KEY `fk_com_opiid` (`opinionid`),
  KEY `fk_rs_com` (`resourceid`),
  CONSTRAINT `complaint_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `user` (`id`),
  CONSTRAINT `complaint_ibfk_2` FOREIGN KEY (`titleId`) REFERENCES `exercise` (`id`),
  CONSTRAINT `fk_author_user` FOREIGN KEY (`authorid`) REFERENCES `user` (`id`),
  CONSTRAINT `fk_com_opiid` FOREIGN KEY (`opinionid`) REFERENCES `opinion` (`id`),
  CONSTRAINT `fk_rs_com` FOREIGN KEY (`resourceid`) REFERENCES `source` (`id`),
  CONSTRAINT `fk_topicid_com` FOREIGN KEY (`topicid`) REFERENCES `topic` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `exercise`
--

DROP TABLE IF EXISTS `exercise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exercise` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `answer` varchar(255) NOT NULL,
  `tips` varchar(255) DEFAULT NULL,
  `userId` int(11) DEFAULT NULL,
  `state` enum('NORMAL','ACTIVE') DEFAULT 'NORMAL',
  `points` int(255) DEFAULT '0',
  `complaint` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `EU_userId` (`userId`),
  CONSTRAINT `EU_userId` FOREIGN KEY (`userId`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `opinion`
--

DROP TABLE IF EXISTS `opinion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opinion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userId` int(11) NOT NULL,
  `topicId` int(11) NOT NULL,
  `opinion` varchar(255) NOT NULL,
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `state` enum('NORMAL','ACTIVE') DEFAULT 'NORMAL',
  `complaint` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `UT_userId` (`userId`),
  KEY `UT_topicId` (`topicId`),
  CONSTRAINT `UT_topicId` FOREIGN KEY (`topicId`) REFERENCES `topic` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `UT_userId` FOREIGN KEY (`userId`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `source`
--

DROP TABLE IF EXISTS `source`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `source` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userId` int(11) NOT NULL,
  `content` int(255) NOT NULL DEFAULT '0',
  `points` int(255) NOT NULL DEFAULT '0',
  `download` varchar(255) NOT NULL,
  `state` enum('NORMAL','ACTIVE') DEFAULT 'NORMAL',
  `complaint` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `SU_userId` (`userId`),
  CONSTRAINT `SU_userId` FOREIGN KEY (`userId`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `topic`
--

DROP TABLE IF EXISTS `topic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `time` datetime NOT NULL,
  `userID` int(11) NOT NULL,
  `replyTime` int(11) NOT NULL DEFAULT '0',
  `modifyTime` datetime NOT NULL,
  `complaint` int(11) DEFAULT '0',
  `state` enum('NORMAL','ACTIVE') DEFAULT 'NORMAL',
  PRIMARY KEY (`id`),
  KEY `name` (`name`),
  KEY `TU_userId` (`userID`),
  CONSTRAINT `TU_userId` FOREIGN KEY (`userID`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `state` enum('NORMAL','ACTIVE') DEFAULT 'ACTIVE',
  `points` int(255) DEFAULT '0',
  `head` varchar(255) DEFAULT NULL,
  `flag` varchar(255) DEFAULT NULL,
  `complaint` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-05-04 22:27:56
