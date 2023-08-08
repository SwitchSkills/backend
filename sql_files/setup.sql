


#DATABASE_SCHEMATIC IS NOT EXACT SIMILAR AS IMPLEMENTED DATABASE IN GOOGLE CLOUD!!!!

CREATE TABLE IF NOT EXISTS users(
    user_id BIGINT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR (50) NOT NULL,
    email_address VARCHAR(150) UNIQUE KEY,
    phone_number VARCHAR(15) NOT NULL UNIQUE KEY,
    alternative_communication VARCHAR(200) NULL DEFAULT NULL,
    bibliography LONGTEXT DEFAULT NULL,
    picture_id BIGINT DEFAULT NULL REFERENCES picture(picture_id) ON DELETE SET NULL ON UPDATE CASCADE ,
    password VARCHAR(200) NOT NULL,
    UNIQUE(first_name,last_name)
);

CREATE TABLE IF NOT EXISTS region(
    region_id BIGINT PRIMARY KEY,
    country VARCHAR(46) NOT NULL,
    INDEX(country)
);

CREATE TABLE IF NOT EXISTS jobs(
    job_id BIGINT PRIMARY KEY NOT NULL, #NO PARTITIONING ON TIME BECAUSE IT DIDN'T ALLOW FOR UNIQUE REQUIREMENT ON JOB_ID
    description LONGTEXT NOT NULL,
    title VARCHAR(200) NOT NULL,
    datetime_made_utc DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    datetime_expires_utc DATETIME DEFAULT NULL,
    region_id BIGINT NOT NULL REFERENCES region(region_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    user_id_owner BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    longitude DECIMAL(9,6) NOT NULL,
    latitude DECIMAL(8,6) NOT NULL,
    INDEX (user_id_owner),
    INDEX (region_id)
);

CREATE TABLE IF NOT EXISTS labels(
    label_name VARCHAR(50) PRIMARY KEY,
    description LONGTEXT DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS picture(
    picture_id BIGINT PRIMARY KEY,
    picture_data LONGBLOB NOT NULL,
    description LONGTEXT DEFAULT NULL,
    user_id BIGINT UNIQUE DEFAULT NULL REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    job_id BIGINT DEFAULT NULL REFERENCES jobs(job_id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX(job_id)
);

CREATE TABLE IF NOT EXISTS user_is_active_in_region(
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    region_id BIGINT REFERENCES region(region_id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX(user_id),
    INDEX(region_id),
    UNIQUE (user_id,region_id)

);

CREATE TABLE IF NOT EXISTS job_needs_labeled_skills(
    job_id BIGINT REFERENCES jobs(job_id) ON DELETE CASCADE ON UPDATE CASCADE,
    label_name VARCHAR(50) REFERENCES labels(label_name) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX(job_id),
    INDEX(label_name),
    UNIQUE(job_id,label_name)
);

CREATE TABLE IF NOT EXISTS users_like_jobs(
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE ,
    job_id BIGINT REFERENCES jobs(job_id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX (user_id),
    INDEX (job_id),
    UNIQUE(user_id,job_id)
);

CREATE TABLE IF NOT EXISTS users_completed_jobs(
    user_id BIGINT REFERENCES users(user_id) ON DELETE NO ACTION ON UPDATE CASCADE,
    job_id BIGINT REFERENCES jobs(job_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    pending BOOLEAN DEFAULT TRUE,
    datetime_request_utc DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    datetime_confirmation_utc DATETIME DEFAULT NULL,
    PRIMARY KEY(user_id,job_id),
    INDEX(user_id),
    INDEX(job_id),
    INDEX(pending)
);



