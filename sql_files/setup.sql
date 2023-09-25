


#DATABASE_SCHEMATIC IS NOT EXACT SIMILAR AS IMPLEMENTED DATABASE IN GOOGLE CLOUD!!!!

CREATE TABLE IF NOT EXISTS users(
    user_id VARCHAR(200) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR (50) NOT NULL,
    email_address VARCHAR(150) UNIQUE KEY,
    phone_number VARCHAR(15) NOT NULL UNIQUE KEY,
    alternative_communication VARCHAR(200) NULL DEFAULT NULL,
    bibliography LONGTEXT DEFAULT NULL,
    password VARCHAR(200) NOT NULL,
    location VARCHAR(200) NOT NULL,
    rating DOUBLE DEFAULT 0,
    number_of_ratings INTEGER DEFAULT 0,
    UNIQUE(first_name,last_name)
);

CREATE TABLE IF NOT EXISTS region(
    region_id VARCHAR(200) PRIMARY KEY,
    region_name VARCHAR(50)  NOT NULL,
    country VARCHAR(46) NOT NULL,
    INDEX(country),
    INDEX(region_name),
    UNIQUE(region_name,country)

);

CREATE TABLE IF NOT EXISTS jobs(
    job_id VARCHAR(200) PRIMARY KEY NOT NULL, #NO PARTITIONING ON TIME BECAUSE IT DIDN'T ALLOW FOR UNIQUE REQUIREMENT ON JOB_ID
    description LONGTEXT NOT NULL,
    title VARCHAR(200) NOT NULL,
    datetime_made_utc DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    datetime_expires_utc DATETIME DEFAULT NULL,
    region_id VARCHAR(200) NOT NULL ,
    user_id_owner VARCHAR(200) NOT NULL ,
    location VARCHAR(200) NOT NULL,
    INDEX (user_id_owner),
    INDEX (region_id),
    UNIQUE (title,region_id,user_id_owner),
     CONSTRAINT job_to_region FOREIGN KEY (region_id)
    REFERENCES region(region_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT job_to_owner FOREIGN KEY (user_id_owner)
    REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS labels(
    label_name VARCHAR(50) PRIMARY KEY,
    description LONGTEXT DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS picture(
    picture_id VARCHAR(200) PRIMARY KEY,
    picture_location_firebase  VARCHAR(1000) NOT NULL,
    description LONGTEXT DEFAULT NULL,
    user_id VARCHAR(200) UNIQUE DEFAULT NULL ,
    job_id VARCHAR(200) DEFAULT NULL ,
    INDEX(job_id),
    CONSTRAINT picture_to_user FOREIGN KEY (user_id)
    REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT picture_to_job FOREIGN KEY (job_id)
    REFERENCES jobs(job_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS user_is_active_in_region(
    user_id VARCHAR(200) ,
    region_id VARCHAR(200) ,
    INDEX(user_id),
    INDEX(region_id),
    UNIQUE (user_id,region_id),
    CONSTRAINT user_to_region FOREIGN KEY (user_id)
    REFERENCES users(user_id)ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT region_to_user FOREIGN KEY (region_id)
    REFERENCES region(region_id) ON DELETE RESTRICT ON UPDATE CASCADE

);

CREATE TABLE IF NOT EXISTS user_has_labeled_skills(
  user_id VARCHAR(200)  ,
  label_name VARCHAR(50)  ,
  CONSTRAINT user_to_label FOREIGN KEY (user_id)
    REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT label_to_user FOREIGN KEY (label_name)
    REFERENCES labels(label_name) ON DELETE RESTRICT ON UPDATE CASCADE,
  INDEX(user_id),
  INDEX(label_name),
  UNIQUE(user_id, label_name)
);

CREATE TABLE IF NOT EXISTS job_needs_labeled_skills(
    job_id VARCHAR(200) ,
    label_name VARCHAR(50),
    INDEX(job_id),
    INDEX(label_name),
    UNIQUE(job_id,label_name),
    CONSTRAINT job_to_label FOREIGN KEY (job_id)
    REFERENCES jobs(job_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT label_to_job FOREIGN KEY (label_name)
    REFERENCES labels(label_name) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS users_like_jobs(
    user_id VARCHAR(200) ,
    job_id VARCHAR(200) ,
    INDEX (user_id),
    INDEX (job_id),
    UNIQUE(user_id,job_id),
    CONSTRAINT user_to_liked_job FOREIGN KEY (user_id)
    REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT liked_job_to_user FOREIGN KEY (job_id)
    REFERENCES jobs(job_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS users_completed_jobs(
    user_id VARCHAR(200)  ,
    job_id VARCHAR(200) ,
    pending BOOLEAN DEFAULT TRUE,
    datetime_request_utc DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    datetime_confirmation_utc DATETIME DEFAULT NULL,
    PRIMARY KEY(user_id,job_id),
    INDEX(user_id),
    INDEX(job_id),
    INDEX(pending),
    CONSTRAINT user_to_completed_job FOREIGN KEY (user_id)
    REFERENCES users(user_id) ON DELETE NO ACTION ON UPDATE CASCADE,
    CONSTRAINT completed_job_to_user FOREIGN KEY (job_id)
    REFERENCES jobs(job_id) ON DELETE RESTRICT ON UPDATE CASCADE
);



