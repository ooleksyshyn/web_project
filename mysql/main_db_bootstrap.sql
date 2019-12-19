-- -----------------------------------------------
-- Table `department`
-- -----------------------------------------------
DROP TABLE IF EXISTS `department`;

CREATE TABLE `department` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255),
  `slug` VARCHAR(255),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `slug_idx`(`slug` ASC)
) ENGINE=InnoDB;


-- -----------------------------------------------
-- Table `employee`
-- -----------------------------------------------
DROP TABLE IF EXISTS `employee`;

CREATE TABLE `employee` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `department_id` INT DEFAULT NULL,
  `name` VARCHAR(255) DEFAULT NULL,
  `surname` VARCHAR(255) DEFAULT NULL,
  `slug` VARCHAR(255),
  `salary` INT DEFAULT NULL,
  `birth_date` DATE,
  PRIMARY KEY (`id`),
  INDEX `department_id_idx`(`department_id` ASC),
  UNIQUE INDEX `slug_idx`(`slug` ASC),
  INDEX `birth_date_index`(`birth_date` ASC),
  CONSTRAINT `deparment_id_fk` 
    FOREIGN KEY (`department_id`) 
    REFERENCES `department` (`id`)
    ON UPDATE CASCADE
    ON DELETE CASCADE
) ENGINE=InnoDB;
