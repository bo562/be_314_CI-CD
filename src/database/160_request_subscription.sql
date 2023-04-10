CREATE TABLE request_subscription (
     request_id            MEDIUMINT NOT NULL,
     subscription_id       MEDIUMINT NOT NULL,
     PRIMARY KEY (request_id, subscription_id),
     FOREIGN KEY (request_id) REFERENCES request(request_id),
     FOREIGN KEY (subscription_id) REFERENCES subscription(subscription_id)
);