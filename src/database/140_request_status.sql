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

