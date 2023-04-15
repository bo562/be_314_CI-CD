CREATE TABLE transaction_status (
     transaction_status_id           INT NOT NULL AUTO_INCREMENT,
     status_name                     VARCHAR(100) NOT NULL,
     PRIMARY KEY (transaction_status_id)
);

CREATE UNIQUE INDEX uc_transaction_status_name ON request_status(status_name);