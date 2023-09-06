
WITH liked_jobs AS (
    SELECT
        job_id
    FROM users_like_jobs
    WHERE
        users_like_jobs.user_id = {user_id}
),
    {completed_jobs},
    {accepted_jobs},
relevant_jobs AS (
SELECT
    jobs.job_id,
    jobs.description AS job_description,
    jobs.title,
    region.region_name,
    region.country,
    jobs.user_id_owner,
    jobs.datetime_made_utc,
    jobs.location AS job_location
FROM jobs
JOIN liked_jobs ON
    liked_jobs.job_id = jobs.job_id
JOIN region ON
    jobs.region_id = region.region_id
WHERE
    jobs.job_id NOT IN (SELECT job_id FROM completed_jobs)
    AND jobs.job_id NOT IN (SELECT job_id FROM accepted_jobs)
),
{job_additional_information}
SELECT
    relevant_jobs.job_id,
    relevant_jobs.datetime_made_utc AS datetime_utc,
    relevant_jobs.title,
    relevant_jobs.job_description,
    relevant_jobs.job_location,
    relevant_jobs.region_name,
    relevant_jobs.country,
    relevant_pictures.picture_location_firebase,
    relevant_pictures.picture_description,
    relevant_labels.label_name,
    relevant_labels.label_description,
    owners.first_name,
    owners.last_name,
    owners.email_address,
    owners.alternative_communication,
    owners.phone_number,
    owners.user_location
FROM relevant_jobs
LEFT JOIN relevant_pictures ON
    relevant_jobs.job_id = relevant_pictures.job_id
LEFT JOIN relevant_labels ON
    relevant_jobs.job_id = relevant_labels.job_id
JOIN owners ON
    relevant_jobs.job_id = owners.job_id
ORDER BY
    relevant_jobs.datetime_made_utc
;