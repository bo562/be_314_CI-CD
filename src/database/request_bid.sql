CREATE TABLE request_bid (
	 request_bid_id               MEDIUMINT NOT NULL AUTO_INCREMENT,
     request_id                   MEDIUMINT NOT NULL,
     professional_id              MEDIUMINT NOT NULL,
     sent_date                    DATETIME NOT NULL,
     accepted_by_client_date      DATETIME,
     professional_cancelled_date  DATETIME,     
     bid_status_id                MEDIUMINT NOT NULL,
     PRIMARY KEY (request_bid_id),
     FOREIGN KEY (professional_id) REFERENCES client(professional_id),
     FOREIGN KEY (request_id) REFERENCES request(request_id)
     FOREIGN KEY (bid_status_id) REFERENCES bid_status(bid_status_id)
);
