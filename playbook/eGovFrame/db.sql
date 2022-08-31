CREATE TABLE `IDS` (
  `table_name` varchar(16) NOT NULL,
  `next_id` decimal(30,0) NOT NULL,
  PRIMARY KEY (`table_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE `SAMPLE` (
  `id` varchar(16) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  `use_yn` char(1) DEFAULT NULL,
  `reg_user` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;


INSERT INTO cloud.SAMPLE (id, name, description, use_yn, reg_user) VALUES('SAMPLE-00001','Runtime Environment','Foundation Layer','Y','eGov');
INSERT INTO cloud.SAMPLE (id, name, description, use_yn, reg_user) VALUES('SAMPLE-00002','Runtime Environment','Persistence Layer','Y','eGov');
INSERT INTO cloud.SAMPLE (id, name, description, use_yn, reg_user) VALUES('SAMPLE-00003','Runtime Environment','Presentation Layer','Y','eGov');
INSERT INTO cloud.SAMPLE (id, name, description, use_yn, reg_user) VALUES('SAMPLE-00004','Runtime Environment','Business Layer','Y','eGov');
INSERT INTO cloud.SAMPLE (id, name, description, use_yn, reg_user) VALUES('SAMPLE-00005','Runtime Environment','Batch Layer','Y','eGov');
INSERT INTO cloud.SAMPLE (id, name, description, use_yn, reg_user) VALUES('SAMPLE-00006','Runtime Environment','Integration Layer','Y','eGov');
INSERT INTO cloud.SAMPLE (id, name, description, use_yn, reg_user) VALUES('SAMPLE-00007','Runtime Environment','Integration Layer','Y','eGov');
INSERT INTO cloud.SAMPLE (id, name, description, use_yn, reg_user) VALUES('SAMPLE-00008','Runtime Environment','Integration Layer','Y','eGov');
INSERT INTO cloud.SAMPLE (id, name, description, use_yn, reg_user) VALUES('SAMPLE-00009','Runtime Environment','Integration Layer','Y','eGov');
INSERT INTO cloud.IDS (table_name, next_id) VALUES('SAMPLE',10);