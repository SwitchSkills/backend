relevant_pictures AS (
SELECT
    relevant_jobs.job_id
    picture.picture_location_firebase,
    picture.description AS picture_description
FROM picture
JOIN relevant_jobs ON
    picture.job_id = relevant_jobs.job_id
)
,
relevant_labels AS (
SELECT
    relevant_users.user_id,
    labels.label_name,
    labels.description AS label_description
FROM labels
JOIN user_has_labeled_skills ON
    user_has_labeled_skills.label_name = labels.label_name
JOIN relevant_users ON
    relevant_users.user_id = user_has_labeled_skilss.user_id
    ),
owners AS (
SELECT
    relevant_jobs.job_id,
    users.first_name,
    users.last_name,
    users.email_address,
    users.alternative_communication,
    users.phone_number,
    users.location AS user_location
FROM users
JOIN relevant_jobs ON
    relevant_jobs.user_id_owner = users.user_id
    )