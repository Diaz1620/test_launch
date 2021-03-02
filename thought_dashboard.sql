-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema thought_dashboard
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema thought_dashboard
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `thought_dashboard` DEFAULT CHARACTER SET utf8 ;
USE `thought_dashboard` ;

-- -----------------------------------------------------
-- Table `thought_dashboard`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `thought_dashboard`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT Now(),
  `updated_at` DATETIME NULL DEFAULT Now(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `thought_dashboard`.`thoughts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `thought_dashboard`.`thoughts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `content` TEXT NULL,
  `created_at` DATETIME NULL DEFAULT Now(),
  `updated_at` DATETIME NULL DEFAULT Now(),
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_thoughts_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_thoughts_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `thought_dashboard`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `thought_dashboard`.`likes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `thought_dashboard`.`likes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `created_at` DATETIME NULL DEFAULT Now(),
  `updated_at` DATETIME NULL DEFAULT Now(),
  `thought_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_likes_thoughts1_idx` (`thought_id` ASC) VISIBLE,
  INDEX `fk_likes_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_likes_thoughts1`
    FOREIGN KEY (`thought_id`)
    REFERENCES `thought_dashboard`.`thoughts` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_likes_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `thought_dashboard`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
