CREATE TABLE request_status (
     request_status_id           INT NOT NULL AUTO_INCREMENT,
     status_name                 VARCHAR(100) NOT NULL,
     PRIMARY KEY (request_status_id)
);

CREATE UNIQUE INDEX uc_request_status_name ON request_status(status_name);