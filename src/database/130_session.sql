CREATE TABLE session (
	 session_id         MEDIUMINT NOT NULL AUTO_INCREMENT,
     authorisation_id   MEDIUMINT NOT NULL,
     expiry_date        DATETIME NOT NULL,
     access_token       VARCHAR(255) NOT NULL,
     PRIMARY KEY (session_id),
     FOREIGN KEY (authorisation_id) REFERENCES authorisation(authorisation_id)
);

