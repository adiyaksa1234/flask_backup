
-- TABLE USER
CREATE TABLE user(
    id INT NOT NULL AUTO_INCREMENT,
    username varchar(150) NOT NULL,
    password varchar(150) NOT NULL,
    email varchar(2500) NOT NULL,
    waktu_buat DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
)