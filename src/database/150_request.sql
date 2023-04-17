CREATE TABLE request (
     request_id         MEDIUMINT NOT NULL AUTO_INCREMENT,
     client_id          MEDIUMINT NOT NULL,
     service_id         INT NOT NULL,
     request_date       DATETIME NOT NULL,
     postcode           INT NOT NULL,
     professional_id    MEDIUMINT,
     start_date         DATETIME,
     completion_date    DATETIME,
     instruction        VARCHAR(4000),
     request_status_id  INT NOT NULL,
     PRIMARY KEY (request_id),
     FOREIGN KEY (client_id) REFERENCES client(client_id),
     FOREIGN KEY (professional_id) REFERENCES professional(professional_id),
     FOREIGN KEY (service_id) REFERENCES service(service_id),
     FOREIGN KEY (request_status_id) REFERENCES request_status(request_status_id)
);