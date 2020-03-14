-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 13, 2020 at 02:01 PM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `flask_all_habibi`
--

-- --------------------------------------------------------

--
-- Table structure for table `animal`
--

CREATE TABLE `animal` (
  `AnimalID` int(11) NOT NULL,
  `AnimalTag` varchar(300) NOT NULL,
  `AnimalCategory` varchar(300) NOT NULL,
  `AnimalBreed` varchar(300) NOT NULL,
  `AnimalSex` varchar(300) NOT NULL,
  `AnimalOwner` varchar(300) NOT NULL,
  `AnimalDOB` varchar(300) NOT NULL,
  `AnimalFather` varchar(300) NOT NULL,
  `AnimalMother` varchar(300) NOT NULL,
  `AnimalWeight` float NOT NULL,
  `AnimalStatus` varchar(300) NOT NULL,
  `AddedDate` varchar(300) NOT NULL,
  `UpdatedDate` varchar(300) NOT NULL,
  `AnimalStatusDate` varchar(300) DEFAULT NULL,
  `AnimalStatusCause` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `animal`
--

INSERT INTO `animal` (`AnimalID`, `AnimalTag`, `AnimalCategory`, `AnimalBreed`, `AnimalSex`, `AnimalOwner`, `AnimalDOB`, `AnimalFather`, `AnimalMother`, `AnimalWeight`, `AnimalStatus`, `AddedDate`, `UpdatedDate`, `AnimalStatusDate`, `AnimalStatusCause`) VALUES
(4, 'GO-OMA-4', 'GOAT', 'OMANI', 'Male', 'Xian', '13-01-2020', 'GO-SAL-66', 'GO-OMA-05', 74.1, 'DIED', '13-03-2020', '13-03-2020', '13-03-2020', 'Normla Death'),
(5, 'GO-OMA-5', 'GOAT', 'OMANI', 'Male', 'Xian', '13-01-2020', 'GO-SAL-1', 'GO-OMA-2', 7.1, 'DIED', '13-03-2020', '13-03-2020', '13-03-2020', 'Normla Death'),
(6, 'HO-BEA-6', 'HORSE', 'BEAUTY', 'Female', 'Nahid', '13-01-2020', 'HO-RAC-11', 'HO-BEA-22', 7.1, 'SLAUGHTER', '13-03-2020', '13-03-2020', '13-03-2020', 'NULL'),
(7, 'SH-PRO-7', 'SHEEP', 'PROJECT', 'Female', 'Nahid', '13-01-2020', 'GO-SAL-11', 'GO-OMA-22', 7.1, 'ALIVE', '13-03-2020', '13-03-2020', NULL, NULL),
(8, 'GO-SAL-8', 'GOAT', 'SALEH', 'Female', 'Nahid', '13-01-2020', 'GO-OMA-101', 'GO-BEA-22', 7.1, 'ALIVE', '13-03-2020', '13-03-2020', NULL, NULL),
(9, 'GO-SAL-9', 'GOAT', 'SALEH', 'Female', 'Xian', '13-01-2020', 'GO-OMA-101', 'GO-BEA-22', 7.1, 'SLAUGHTER', '13-03-2020', '13-03-2020', '13-03-2020', 'NULL'),
(10, 'GO-SAL-10', 'GOAT', 'SALEH', 'Female', 'Xian', '13-01-2020', 'GO-OMA-101', 'GO-BEA-22', 7.1, 'SLAUGHTER', '13-03-2020', '13-03-2020', '13-03-2020', 'NULL'),
(11, 'GO-SAL-11', 'GOAT', 'SALEH', 'Female', 'Xian', '13-01-2020', 'GO-OMA-101', 'GO-BEA-22', 7.1, 'SLAUGHTER', '13-03-2020', '13-03-2020', '13-03-2020', 'NULL'),
(12, 'GO-SAL-12', 'GOAT', 'SALEH', 'Female', 'Xian', '13-01-2020', 'GO-OMA-101', 'GO-BEA-22', 7.1, 'ALIVE', '13-03-2020', '13-03-2020', NULL, NULL),
(13, 'GO-SAL-13', 'GOAT', 'SALEH', 'Female', 'Xian', '13-01-2020', 'GO-OMA-101', 'GO-BEA-22', 7.1, 'ALIVE', '13-03-2020', '13-03-2020', NULL, NULL),
(14, 'GO-SAL-14', 'GOAT', 'SALEH', 'Female', 'Xian', '13-01-2020', 'GO-OMA-101', 'GO-BEA-22', 7.1, 'SLAUGHTER', '13-03-2020', '13-03-2020', '13-03-2020', 'NULL');

-- --------------------------------------------------------

--
-- Table structure for table `animalcategory`
--

CREATE TABLE `animalcategory` (
  `AcID` int(11) NOT NULL,
  `AcCat` varchar(300) NOT NULL,
  `AcSubCat` varchar(300) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `animalcategory`
--

INSERT INTO `animalcategory` (`AcID`, `AcCat`, `AcSubCat`) VALUES
(1, 'Goat', 'OMANI'),
(2, 'Goat', 'SHAMMAL'),
(3, 'Goat', 'NORMAL GOAT'),
(4, 'Sheep', 'TALLAL'),
(5, 'Sheep', 'SIMON'),
(6, 'Sheep', 'SALEH'),
(7, 'Sheep', 'ROBBY'),
(8, 'Sheep', 'BARBI'),
(9, 'Sheep', 'HARRYAT'),
(10, 'Sheep', 'PROJECT'),
(11, 'Horse', 'BEAUTY'),
(12, 'Horse', 'RACING'),
(13, 'Camel', 'BIG'),
(14, 'Camel', 'SMALL');

-- --------------------------------------------------------

--
-- Table structure for table `animalpicture`
--

CREATE TABLE `animalpicture` (
  `AnimalPictureID` int(11) NOT NULL,
  `AnimalID` int(11) NOT NULL,
  `AnimalPictureBlob` blob DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `animalpicture`
--

INSERT INTO `animalpicture` (`AnimalPictureID`, `AnimalID`, `AnimalPictureBlob`) VALUES
(1, 1, 0x4e554c4c),
(2, 4, 0x4e554c4c),
(3, 5, 0x4e554c4c),
(4, 6, 0x4e554c4c),
(5, 7, 0x4e554c4c),
(6, 8, 0x4e554c4c),
(7, 9, 0x4e554c4c),
(8, 10, 0x4e554c4c),
(9, 11, 0x4e554c4c),
(10, 12, 0x4e554c4c),
(11, 13, 0x4e554c4c),
(12, 14, 0x4e554c4c);

-- --------------------------------------------------------

--
-- Table structure for table `commondata`
--

CREATE TABLE `commondata` (
  `CdID` int(11) NOT NULL,
  `TotalGoat` int(11) NOT NULL,
  `TotalSheep` int(11) NOT NULL,
  `TotalCamel` int(11) NOT NULL,
  `TotalHorse` int(11) NOT NULL,
  `DiedGoat` int(11) NOT NULL,
  `DiedSheep` int(11) NOT NULL,
  `DiedCamel` int(11) NOT NULL,
  `DiedHorse` int(11) NOT NULL,
  `SlaughterGoat` int(11) NOT NULL,
  `SlaughterSheep` int(11) NOT NULL,
  `SlaughterCamel` int(11) NOT NULL,
  `SlaughterHorse` int(11) NOT NULL,
  `MissingGoat` int(11) NOT NULL,
  `MissingSheep` int(11) NOT NULL,
  `MissingCamel` int(11) NOT NULL,
  `MissingHorse` int(11) NOT NULL,
  `Owner` int(11) NOT NULL,
  `Employee` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `commondata`
--

INSERT INTO `commondata` (`CdID`, `TotalGoat`, `TotalSheep`, `TotalCamel`, `TotalHorse`, `DiedGoat`, `DiedSheep`, `DiedCamel`, `DiedHorse`, `SlaughterGoat`, `SlaughterSheep`, `SlaughterCamel`, `SlaughterHorse`, `MissingGoat`, `MissingSheep`, `MissingCamel`, `MissingHorse`, `Owner`, `Employee`) VALUES
(1, 4, 1, 0, 0, 2, 0, 0, 0, 4, 0, 0, 1, 0, 0, 0, 0, 2, 3);

-- --------------------------------------------------------

--
-- Table structure for table `owner`
--

CREATE TABLE `owner` (
  `OwnerID` int(11) NOT NULL,
  `OwnerName` varchar(300) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `owner`
--

INSERT INTO `owner` (`OwnerID`, `OwnerName`) VALUES
(1, 'Xian'),
(2, 'Nahid');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `UserID` int(11) NOT NULL,
  `UserName` varchar(300) NOT NULL,
  `UserPhone` varchar(300) NOT NULL,
  `UserEmail` varchar(300) NOT NULL,
  `UserPass` varchar(300) NOT NULL,
  `UserAddress` varchar(300) NOT NULL,
  `AddedDate` varchar(300) NOT NULL,
  `UpdateDate` varchar(300) NOT NULL,
  `Type` varchar(300) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `vaccinedetails`
--

CREATE TABLE `vaccinedetails` (
  `VID` int(11) NOT NULL,
  `AnimalTag` varchar(300) NOT NULL,
  `VDetails` varchar(1000) NOT NULL,
  `VDate` varchar(300) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vaccinedetails`
--

INSERT INTO `vaccinedetails` (`VID`, `AnimalTag`, `VDetails`, `VDate`) VALUES
(1, 'HO-BEA-6', '13-03-2020', 'bideshi vaccine disi ostaad');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `animal`
--
ALTER TABLE `animal`
  ADD PRIMARY KEY (`AnimalID`);

--
-- Indexes for table `animalcategory`
--
ALTER TABLE `animalcategory`
  ADD PRIMARY KEY (`AcID`);

--
-- Indexes for table `animalpicture`
--
ALTER TABLE `animalpicture`
  ADD PRIMARY KEY (`AnimalPictureID`);

--
-- Indexes for table `commondata`
--
ALTER TABLE `commondata`
  ADD PRIMARY KEY (`CdID`);

--
-- Indexes for table `owner`
--
ALTER TABLE `owner`
  ADD PRIMARY KEY (`OwnerID`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`UserID`);

--
-- Indexes for table `vaccinedetails`
--
ALTER TABLE `vaccinedetails`
  ADD PRIMARY KEY (`VID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `animal`
--
ALTER TABLE `animal`
  MODIFY `AnimalID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `animalcategory`
--
ALTER TABLE `animalcategory`
  MODIFY `AcID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `animalpicture`
--
ALTER TABLE `animalpicture`
  MODIFY `AnimalPictureID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `commondata`
--
ALTER TABLE `commondata`
  MODIFY `CdID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `owner`
--
ALTER TABLE `owner`
  MODIFY `OwnerID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `UserID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `vaccinedetails`
--
ALTER TABLE `vaccinedetails`
  MODIFY `VID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
