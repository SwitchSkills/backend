relevant_pictures_users AS (
SELECT
    relevant_user_ids.user_id,
    picture.picture_data,
    picture.description AS picture_description
FROM picture
JOIN relevant_users ON
    relevant_users.user_id = picture.user_id
    )
relevant_labels_user AS (
SELECT
    relevant_jobs.job_id,
    labels.label_name,
    labels.description AS label_description
FROM labels
JOIN job_need_labeled_skills ON
    job_need_labeled_skills.label_name = labels.label_name
JOIN relevant_jobs ON
    relevant_jobs.job_id = job_need_labeled_skills.job_id
)