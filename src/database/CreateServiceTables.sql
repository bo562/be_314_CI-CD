CREATE TABLE service (
	 service_id         MEDIUMINT NOT NULL AUTO_INCREMENT,
     service_name       VARCHAR(255) NOT NULL,
     cost               DECIMAL(10,2) NOT NULL,
     retired            DATETIME NOT NULL,
     PRIMARY KEY (service_id)
);
CREATE UNIQUE INDEX uc_service_name ON service(service_name, retired);
 
-- ToDo: rename table to provided_service
CREATE TABLE associated_service (
	 provided_service_id MEDIUMINT NOT NULL AUTO_INCREMENT,
     service_id          MEDIUMINT NOT NULL,
     professional_id     MEDIUMINT NOT NULL,
     PRIMARY KEY (provided_service_id),
     FOREIGN KEY (service_id) REFERENCES service(service_id),
     FOREIGN KEY (professional_id) REFERENCES professional(professional_id)
);
CREATE UNIQUE INDEX uc_associated_service ON 
	associated_service(professional_id, service_id);
