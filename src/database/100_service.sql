CREATE TABLE service (
     service_id         INT NOT NULL AUTO_INCREMENT,
     service_name       VARCHAR(255) NOT NULL,
     retired            DATETIME,
     PRIMARY KEY (service_id)
);

CREATE UNIQUE INDEX uc_service_name ON service(service_name, retired);
