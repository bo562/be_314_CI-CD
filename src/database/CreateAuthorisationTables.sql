CREATE TABLE authorisation (
	 authorisation_id   MEDIUMINT NOT NULL AUTO_INCREMENT,
     user_id            MEDIUMINT NOT NULL,
     refresh_token      VARCHAR(255) NOT NULL,
     number_of_uses     INT NOT NULL,   
     invalidated        ENUM('Y','N') NOT NULL,
     PRIMARY KEY (authorisation_id),
     FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE session (
	 session_id         MEDIUMINT NOT NULL AUTO_INCREMENT,
     authorisation_id   MEDIUMINT NOT NULL,
     expiry_date        DATETIME NOT NULL,
     access_token       VARCHAR(255) NOT NULL,
     PRIMARY KEY (session_id),
     FOREIGN KEY (authorisation_id) REFERENCES authorisation(authorisation_id)
);
