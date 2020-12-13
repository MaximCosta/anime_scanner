SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema anime
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `anime` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci ;
USE `anime` ;

-- -----------------------------------------------------
-- Table `anime`.`categorie_lang`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `anime`.`categorie_lang` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_general_ci;


-- -----------------------------------------------------
-- Table `anime`.`anime`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `anime`.`anime` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL DEFAULT NULL,
  `image` VARCHAR(255) NULL DEFAULT NULL,
  `duree` VARCHAR(45) NULL DEFAULT NULL,
  `saison` INT NULL DEFAULT NULL,
  `desc` TEXT NULL DEFAULT NULL,
  `update` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `categorie_lang_id` INT NOT NULL,
  PRIMARY KEY (`id`, `categorie_lang_id`),
  UNIQUE INDEX `name_saison_UNIQUE` (`name` ASC, `saison` ASC) VISIBLE,
  INDEX `fk_anime_categorie1_idx` (`categorie_lang_id` ASC) VISIBLE,
  CONSTRAINT `fk_anime_categorie1`
    FOREIGN KEY (`categorie_lang_id`)
    REFERENCES `anime`.`categorie_lang` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_general_ci;


-- -----------------------------------------------------
-- Table `anime`.`type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `anime`.`type` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 26
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_general_ci;


-- -----------------------------------------------------
-- Table `anime`.`anime_has_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `anime`.`anime_has_type` (
  `anime_id` INT NOT NULL,
  `type_id` INT NOT NULL,
  PRIMARY KEY (`anime_id`, `type_id`),
  INDEX `fk_anime_has_type_type1_idx` (`type_id` ASC) VISIBLE,
  INDEX `fk_anime_has_type_anime_idx` (`anime_id` ASC) VISIBLE,
  CONSTRAINT `fk_anime_has_type_anime`
    FOREIGN KEY (`anime_id`)
    REFERENCES `anime`.`anime` (`id`),
  CONSTRAINT `fk_anime_has_type_type1`
    FOREIGN KEY (`type_id`)
    REFERENCES `anime`.`type` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_general_ci;


-- -----------------------------------------------------
-- Table `anime`.`episode`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `anime`.`episode` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `numero` VARCHAR(20) NULL DEFAULT NULL,
  `anime_id` INT NOT NULL,
  PRIMARY KEY (`id`, `anime_id`),
  UNIQUE INDEX `numero_anime_id_UNIQUE` (`numero` ASC, `anime_id` ASC) VISIBLE,
  INDEX `fk_episode_anime1_idx` (`anime_id` ASC) VISIBLE,
  CONSTRAINT `fk_episode_anime1`
    FOREIGN KEY (`anime_id`)
    REFERENCES `anime`.`anime` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_general_ci;


-- -----------------------------------------------------
-- Table `anime`.`lecteur`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `anime`.`lecteur` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  `go` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_general_ci;


-- -----------------------------------------------------
-- Table `anime`.`episode_lecteur`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `anime`.`episode_lecteur` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `episode_id` INT NOT NULL,
  `lecteur_id` INT NOT NULL,
  `link` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`id`, `episode_id`, `lecteur_id`),
  INDEX `fk_episode_lecteur_episode1_idx` (`episode_id` ASC) VISIBLE,
  INDEX `fk_episode_lecteur_lecteur1_idx` (`lecteur_id` ASC) VISIBLE,
  CONSTRAINT `fk_episode_lecteur_episode1`
    FOREIGN KEY (`episode_id`)
    REFERENCES `anime`.`episode` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `fk_episode_lecteur_lecteur1`
    FOREIGN KEY (`lecteur_id`)
    REFERENCES `anime`.`lecteur` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_general_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
