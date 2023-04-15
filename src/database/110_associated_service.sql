-- ToDo: rename table to provided_service
CREATE TABLE associated_service (
     provided_service_id MEDIUMINT NOT NULL AUTO_INCREMENT,
     service_id          INT NOT NULL,
     professional_id     MEDIUMINT NOT NULL,
     PRIMARY KEY (provided_service_id),
     FOREIGN KEY (service_id) REFERENCES service(service_id),
     FOREIGN KEY (professional_id) REFERENCES professional(professional_id)
);
CREATE UNIQUE INDEX uc_associated_service ON 
    associated_service(professional_id, service_id);