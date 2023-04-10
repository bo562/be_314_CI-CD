CREATE TABLE request_transaction (
	 request_id           MEDIUMINT NOT NULL,
     transaction_id       MEDIUMINT NOT NULL,
     PRIMARY KEY (request_id, transaction_id),
     FOREIGN KEY (request_id) REFERENCES request(request_id),
     FOREIGN KEY (transaction_id) REFERENCES transaction(transaction_id)
);

