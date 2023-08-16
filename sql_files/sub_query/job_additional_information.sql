relevant_pictures AS (
SELECT
    relevant_jobs.job_id
    picture.picture_data,
    picture.description AS picture_description
FROM picture
JOIN relevant_jobs ON
    picture.job_id = relevant_jobs.job_id
)
,
relevant_labels AS (
SELECT
    relevant_jobs.job_id,
    labels.label_name,
    labels.description AS label_description
FROM labels
JOIN job_need_labeled_skills ON
    job_need_labeled_skills.label_name = labels.label_name
JOIN relevant_jobs ON
    relevant_jobs.job_id = job_need_labeled_skills.job_id
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