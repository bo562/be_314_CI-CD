CREATE TABLE request (
	 request_id         MEDIUMINT NOT NULL AUTO_INCREMENT,
     client_id          MEDIUMINT NOT NULL,
     service_id         MEDIUMINT NOT NULL,
     request_date       DATETIME NOT NULL,
     professional_id    MEDIUMINT,
     start_date         DATETIME,
     completion_date    DATETIME,
     instruction        VARCHAR(4000),
     request_status_id  MEDIUMINT NOT NULL 
     PRIMARY KEY (request_id),
     FOREIGN KEY (client_id) REFERENCES client(client_id),
     FOREIGN KEY (professional_id) REFERENCES client(professional_id),
     FOREIGN KEY (service_id) REFERENCES service(service_id)
);

CREATE TABLE request_status (
	 request_status_id           MEDIUMINT NOT NULL,
     status_name                 VARCHAR(100) NOT NULL,
     PRIMARY KEY (request_status_id),
);
CREATE UNIQUE INDEX uc_request_status_name ON request_status(status_name);

INSERT INTO bid_status (request_status_id, status_name) values (1, 'Open');
INSERT INTO bid_status (request_status_id, status_name) values (2, 'Assigned');
INSERT INTO bid_status (request_status_id, status_name) values (3, 'In progress');
INSERT INTO bid_status (request_status_id, status_name) values (3, 'Completed - not paid');
INSERT INTO bid_status (request_status_id, status_name) values (3, 'Completed');
INSERT INTO bid_status (request_status_id, status_name) values (4, 'Cancelled');
COMMIT;