CREATE DATABASE `bloomdb`

use `bloomdb`;

CREATE TABLE `accounts` (
  `firstName` varchar(255) DEFAULT NULL,
  `lastName` varchar(255) DEFAULT NULL,
  `userName` varchar(255) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `isOwner` varchar(255) DEFAULT NULL,
  `token` varchar(255) DEFAULT NULL,
  `age` varchar(255) DEFAULT NULL,
  `gender` varchar(255) DEFAULT NULL,
  `isAvailable` varchar(255) DEFAULT NULL,
  `bio` varchar(255) DEFAULT NULL,
  `categoryType` varchar(255) DEFAULT NULL,
  `categoryLevel` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`userName`)
)


CREATE TABLE `venue` (
  `venueId` int NOT NULL,
  `venueDescription` varchar(255) DEFAULT NULL,
  `venueAddress` varchar(255) DEFAULT NULL,
  `venueOwner` varchar(255) DEFAULT NULL,
  `venueName` varchar(255) DEFAULT NULL,
  `venueAvailability` varchar(255) DEFAULT NULL,
  `venueOpen` varchar(255) DEFAULT NULL,
  `venueHrCost` int DEFAULT NULL,
  `venueCategory` varchar(255) DEFAULT NULL,
  `venueCity` varchar(255) DEFAULT NULL,
  `venueState` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`venueId`)
)

CREATE TABLE `venueimages` (
  `imageId` int NOT NULL AUTO_INCREMENT,
  `venueId` int DEFAULT NULL,
  `venueImage` longblob,
  PRIMARY KEY (`imageId`),
  KEY `venueId` (`venueId`),
  CONSTRAINT `venueimages_ibfk_1` FOREIGN KEY (`venueId`) REFERENCES `venue` (`venueId`)
) 

CREATE TABLE `venueRating` (
  `venueId` int NOT NULL,
  `userName` varchar(50) NOT NULL,
  `rating` int DEFAULT NULL,
  `review` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`venueId`,`userName`)
)

CREATE TABLE `booking` (
  `venueId` int NOT NULL,
  `venuedate` varchar(255) NOT NULL,
  `venueslots` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`venueId`,`venuedate`)
) 

CREATE TABLE `storeimages` (
  `imageId` int NOT NULL AUTO_INCREMENT,
  `activityId` int DEFAULT NULL,
  `activityImage` longblob,
  PRIMARY KEY (`imageId`),
  KEY `activityId` (`activityId`),
  CONSTRAINT `storeimages_ibfk_1` FOREIGN KEY (`activityId`) REFERENCES `activities` (`activityId`)
)


CREATE TABLE `activities` (
  `activityId` int NOT NULL,
  `activityName` text,
  `activityDescription` text,
  `activityCapacity` int DEFAULT NULL,
  `activityLocation` text,
  `activityCategory` text,
  `activityRemainingCapacity` int DEFAULT NULL,
  `activityAgeRange` text,
  `activityCost` text,
  `activityCostAmount` int DEFAULT NULL,
  `activityOrganizer` text,
  `activityVenueId` int DEFAULT NULL,
  `activityDate` text,
  `activityTime` json DEFAULT NULL,
  `activityVenueCost` int DEFAULT NULL,
  `activityBookingDate` text,
  PRIMARY KEY (`activityId`)
)


CREATE TABLE `bookmark` (
  `userName` varchar(255) NOT NULL,
  `favVenue` varchar(255) DEFAULT NULL,
  `favActivity` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`userName`)
)

CREATE TABLE `activityPayment` (
  `paymentid` int NOT NULL AUTO_INCREMENT,
  `activityId` int DEFAULT NULL,
  `participantuserName` varchar(50) DEFAULT NULL,
  `organizeruserName` varchar(50) DEFAULT NULL,
  `amount` int DEFAULT NULL,
  PRIMARY KEY (`paymentid`),
  KEY `participantuserName` (`participantuserName`),
  KEY `activityId` (`activityId`),
  KEY `organizeruserName` (`organizeruserName`),
  CONSTRAINT `activitypayment_ibfk_1` FOREIGN KEY (`participantuserName`) REFERENCES `Accounts` (`userName`),
  CONSTRAINT `activitypayment_ibfk_2` FOREIGN KEY (`activityId`) REFERENCES `Activities` (`activityId`),
  CONSTRAINT `activitypayment_ibfk_3` FOREIGN KEY (`organizeruserName`) REFERENCES `Accounts` (`userName`)
) 

CREATE TABLE `regact` (
  `activityId` int NOT NULL,
  `userName` varchar(50) NOT NULL,
  PRIMARY KEY (`activityId`,`userName`),
  KEY `regact_ibfk_2` (`userName`),
  CONSTRAINT `regact_ibfk_1` FOREIGN KEY (`activityId`) REFERENCES `activities` (`activityId`),
  CONSTRAINT `regact_ibfk_2` FOREIGN KEY (`userName`) REFERENCES `accounts` (`userName`)
);

CREATE TABLE `activityRating` (
  `reviewId` int NOT NULL AUTO_INCREMENT,
  `activityId` int DEFAULT NULL,
  `userName` varchar(50) DEFAULT NULL,
  `rating` int DEFAULT NULL,
  `review` text,
  PRIMARY KEY (`reviewId`),
  KEY `activityId` (`activityId`),
  KEY `userName` (`userName`),
  CONSTRAINT `activityrating_ibfk_1` FOREIGN KEY (`activityId`) REFERENCES `Activities` (`activityId`),
  CONSTRAINT `activityrating_ibfk_2` FOREIGN KEY (`userName`) REFERENCES `Accounts` (`userName`)
)
