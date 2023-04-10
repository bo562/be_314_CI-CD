CREATE TABLE user_question (
     user_question_id     MEDIUMINT NOT NULL AUTO_INCREMENT,
     user_id              MEDIUMINT NOT NULL,
     security_question_id MEDIUMINT NOT NULL,
     answer               VARCHAR(2000) NOT NULL,
     PRIMARY KEY (user_question_id),
     FOREIGN KEY (security_question_id) REFERENCES security_question(security_question_id),
     FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE UNIQUE INDEX uc_user_question_question ON user_question(user_id, security_question_id);