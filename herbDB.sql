CREATE DATABASE herbDB character set UTF8 collate utf8_vietnamese_ci;

CREATE TABLE IF NOT EXISTS `herbDB`.`herb` (
    `herb_No` INT AUTO_INCREMENT,
    `herb_name` VARCHAR(255) NOT NULL,
    `herb_desc` VARCHAR(255),
    PRIMARY KEY (`herb_No`)
);

INSERT INTO `herbDB`.`herb` (`herb_name`,`herb_desc`)
VALUES ("Bạch Phục Linh",""),
("Cam Thảo", ""),
("Cầu Kỳ Tử", ""),
("Đỗ Trọng", ""),
("Hồng Táo", ""),
("Trạch Tả", "");
