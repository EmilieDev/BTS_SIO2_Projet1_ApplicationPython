CREATE TABLE `Roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `libelleRole` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Services` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `libelleServ` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Specialites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `libelleSpec` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Personnel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nomSoignant` varchar(100),
  `prenomSoignant` varchar(100),
  `idSpecialite` int(11),
  `idService` int(11),
  `idRole` int(11),
  PRIMARY KEY (`id`),
  FOREIGN KEY (`idRole`) REFERENCES `Roles`(`id`),
  FOREIGN KEY (`idService`) REFERENCES `Services`(`id`),
  FOREIGN KEY (`idSpecialite`) REFERENCES `Specialites`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Chirurgiens` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idRoles` int(11) NOT NULL,
  `idPersonnel` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_chir_roles` (`idRoles`),
  KEY `fk_chir_personnel` (`idPersonnel`),
  FOREIGN KEY (`idPersonnel`) REFERENCES `Personnel`(`id`),
  FOREIGN KEY (`idRoles`) REFERENCES `Roles`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Organismes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nomOrg` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `TypeEtudes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `libelleEtu` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Protocole` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `libelleProtocole` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
  FOREIGN KEY (`idTypeEtude`) REFERENCES `TypeEtudes`(`id`),
  FOREIGN KEY (`idOrganisme`) REFERENCES `Organismes`(`id`),
  FOREIGN KEY (`idMedResponsable`) REFERENCES `Personnel`(`id`),
  FOREIGN KEY (`idProtocole`) REFERENCES `Protocole`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Patients` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nomPat` varchar(100) DEFAULT NULL,
  `prenomPat` varchar(100) DEFAULT NULL,
  `dateNaisPat` date DEFAULT NULL,
  `sexe` char(1) DEFAULT NULL,
  `numDossierClinique` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numDossierClinique` (`numDossierClinique`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Maladies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nomMaladie` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Organes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nomOrgane` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Stades` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nomStade` varchar(5) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `EtatInclusion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `libelleEtat` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `DetailEtude` (
  `idPatient` int(11) NOT NULL,
  `idEtude` int(11) NOT NULL,
  `idEtatInclusion` int(11) DEFAULT NULL,
  `dateInclusion` date DEFAULT NULL,
  `idMaladie` int(11) DEFAULT NULL,
  PRIMARY KEY (`idPatient`,`idEtude`),
  FOREIGN KEY (`idPatient`) REFERENCES `Patients`(`id`),
  FOREIGN KEY (`idEtude`) REFERENCES `Etudes`(`id`),
  FOREIGN KEY (`idEtatInclusion`) REFERENCES `EtatInclusion`(`id`),
  FOREIGN KEY (`idMaladie`) REFERENCES `Maladies`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Patients_Maladies` (
  `idPatient` int(11) NOT NULL,
  `idMaladie` int(11) NOT NULL,
  `idOrganes` int(11) DEFAULT NULL,
  `idStade` int(11) DEFAULT NULL,
  `dateDiagnostic` date NOT NULL,
  PRIMARY KEY (`idPatient`,`idMaladie`,`dateDiagnostic`),
  FOREIGN KEY (`idPatient`) REFERENCES `Patients`(`id`),
  FOREIGN KEY (`idMaladie`) REFERENCES `Maladies`(`id`),
  FOREIGN KEY (`idOrganes`) REFERENCES `Organes`(`id`),
  FOREIGN KEY (`idStade`) REFERENCES `Stades`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Questionnaire` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Utilisateurs` (
  `identifiant` int(11) NOT NULL AUTO_INCREMENT,
  `nomUtilisateur` varchar(100) NOT NULL,
  `motDePasse` varchar(255) NOT NULL,
  PRIMARY KEY (`identifiant`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
