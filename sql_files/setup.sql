


#DATABASE_SCHEMATIC IS NOT EXACT SIMILAR AS IMPLEMENTED DATABASE IN GOOGLE CLOUD!!!!

CREATE TABLE IF NOT EXISTS users(
    user_id VARCHAR(200) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR (50) NOT NULL,
    email_address VARCHAR(150) UNIQUE KEY,
    phone_number VARCHAR(15) NOT NULL UNIQUE KEY,
    alternative_communication VARCHAR(200) NULL DEFAULT NULL,
    bibliography LONGTEXT DEFAULT NULL,
    picture_id VARCHAR(200) DEFAULT NULL REFERENCES picture(picture_id) ON DELETE SET NULL ON UPDATE CASCADE ,
    password VARCHAR(200) NOT NULL,
    location VARCHAR(200) NOT NULL,
    rating INTEGER DEFAULT 0,
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
    title VARCHAR(200) UNIQUE NOT NULL,
    datetime_made_utc DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    datetime_expires_utc DATETIME DEFAULT NULL,
    region_id VARCHAR(200) NOT NULL REFERENCES region(region_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    user_id_owner VARCHAR(200) NOT NULL REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    location VARCHAR(200) NOT NULL,
    INDEX (user_id_owner),
    INDEX (region_id)
);

CREATE TABLE IF NOT EXISTS labels(
    label_name VARCHAR(50) PRIMARY KEY,
    description LONGTEXT DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS picture(
    picture_id VARCHAR(200) PRIMARY KEY,
    picture_location_firebase  VARCHAR(200) NOT NULL,
    description LONGTEXT DEFAULT NULL,
    user_id VARCHAR(200) UNIQUE DEFAULT NULL REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    job_id VARCHAR(200) DEFAULT NULL REFERENCES jobs(job_id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX(job_id)
);

CREATE TABLE IF NOT EXISTS user_is_active_in_region(
    user_id VARCHAR(200) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    region_id VARCHAR(200) REFERENCES region(region_id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX(user_id),
    INDEX(region_id),
    UNIQUE (user_id,region_id)

);

CREATE TABLE IF NOT EXISTS user_has_labeled_skills(
  user_id VARCHAR(200) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
  label_name VARCHAR(50) REFERENCES labels(label_name) ON DELETE RESTRICT ON UPDATE CASCADE,
  INDEX(user_id),
  INDEX(label_name)
);

CREATE TABLE IF NOT EXISTS job_needs_labeled_skills(
    job_id VARCHAR(200) REFERENCES jobs(job_id) ON DELETE CASCADE ON UPDATE CASCADE,
    label_name VARCHAR(50) REFERENCES labels(label_name) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX(job_id),
    INDEX(label_name),
    UNIQUE(job_id,label_name)
);

CREATE TABLE IF NOT EXISTS users_like_jobs(
    user_id VARCHAR(200) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE ,
    job_id VARCHAR(200) REFERENCES jobs(job_id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX (user_id),
    INDEX (job_id),
    UNIQUE(user_id,job_id)
);

CREATE TABLE IF NOT EXISTS users_completed_jobs(
    user_id VARCHAR(200) REFERENCES users(user_id) ON DELETE NO ACTION ON UPDATE CASCADE,
    job_id VARCHAR(200) REFERENCES jobs(job_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    pending BOOLEAN DEFAULT TRUE,
    datetime_request_utc DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    datetime_confirmation_utc DATETIME DEFAULT NULL,
    PRIMARY KEY(user_id,job_id),
    INDEX(user_id),
    INDEX(job_id),
    INDEX(pending)
);



