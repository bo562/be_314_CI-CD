CREATE TABLE service (
	 service_id         MEDIUMINT NOT NULL AUTO_INCREMENT,
     service_name       VARCHAR(255) NOT NULL,
     cost               DECIMAL(10,2) NOT NULL,
     retired            DATETIME NOT NULL,
     PRIMARY KEY (service_id)
);
CREATE UNIQUE INDEX uc_service_name ON service(service_name, retired);

INSERT INTO service (service_name,  cost, retired) values ('Lawn mowing', 120, null);
INSERT INTO service (service_name,  cost, retired) values ('Weeding', 130, null);
INSERT INTO service (service_name,  cost, retired) values ('Mulching', 150, null);
INSERT INTO service (service_name,  cost, retired) values ('Plumbing Repair', 220, null);
INSERT INTO service (service_name,  cost, retired) values ('Electrical Repair', 250, null);
INSERT INTO service (service_name,  cost, retired) values ('Whitegoods Installation', 110, null);
INSERT INTO service (service_name,  cost, retired) values ('Locks changed', 170, null);
INSERT INTO service (service_name,  cost, retired) values ('Cleaning', 190, null);
commit;

