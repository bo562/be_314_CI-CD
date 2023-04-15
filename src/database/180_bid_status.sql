CREATE TABLE bid_status (
     bid_status_id               MEDIUMINT NOT NULL,
     status_name                 VARCHAR(100) NOT NULL,
     PRIMARY KEY (bid_status_id),
);

CREATE UNIQUE INDEX uc_bid_status_name ON bid_status(status_name);