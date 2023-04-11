-- TODO: Drop subscription_name
CREATE TABLE subscription (
	 subscription_id    MEDIUMINT NOT NULL AUTO_INCREMENT,
     user_id            MEDIUMINT NOT NULL,
     subscription_name  CHAR(100),
     fee                DECIMAL(10,2) NOT NULL,
     start_date         DATETIME NOT NULL,
     end_date           DATETIME,
     PRIMARY KEY (subscription_id),
     FOREIGN KEY (user_id) REFERENCES user(user_id)
);
CREATE INDEX idx_subscription_user ON subscription(subscription_id, user_id);
CREATE UNIQUE INDEX idx_subscription_user_start ON subscription(user_id, start_date);

