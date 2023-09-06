WITH relevant_regions AS (
SELECT
    region_id,
    region_name,
    country
FROM region
WHERE
    region_id IN {region_id_list}
),
{accepted_jobs},
relevant_jobs AS (
SELECT
    jobs.job_id,
    jobs.description AS job_description,
    jobs.title,
    relevant_regions.region_name,
    relevant_regions.country,
    jobs.user_id_owner,
    jobs.location AS job_location
FROM jobs
JOIN relevant_regions ON
    jobs.region_id = relevant_regions.region_id
WHERE
    jobs.job_id IN (SELECT job_id FROM accepted_jobs)
),
relevant_users AS (
SELECT
    user_is_active_in_region.user_id,
    relevant_regions.region_name,
    relevant_regions.country
FROM relevant_regions
JOIN user_is_active_in_region ON
    user_is_active_in_region.region_id = relevant_regions.region_id
    AND user_is_active_in_region.user_id IN (SELECT user_id FROM accepted_jobs)
    ),
helper_information AS (
SELECT
    accepted_jobs.job_id,
    accepted_jobs.datetime_confirmation_utc,
    users.first_name,
    users.last_name,
    users.email_address,
    users.phone_number,
    users.alternative_communication,
    users.location AS user_location
FROM users
JOIN relevant_users ON
    users.user_id = relevant_users.user_id
JOIN accepted_jobs ON
    accepted_jobs.user_id = users.user_id
    ),
{job_additional_information}
SELECT
    relevant_jobs.job_id,
    helper_information.datetime_confirmation_utc AS datetime_utc,
    relevant_jobs.title,
    relevant_jobs.job_description,
    relevant_jobs.job_location,
    relevant_jobs.region_name,
    relevant_jobs.country,
    relevant_pictures.picture_location_firebase,
    relevant_pictures.picture_description,
    relevant_labels.label_name,
    relevant_labels.label_description,
    owners.first_name AS owner_first_name,
    owners.last_name AS owner_last_name,
    owners.email_address AS owner_email_address,
    owners.alternative_communication AS owner_alternative_communication,
    owners.phone_number AS owner_phone_number,
    owners.user_location AS owner_location,
    helper_information.first_name AS helper_first_name,
    helper_information.last_name AS helper_last_name,
    helper_information.email_address AS helper_email_address,
    helper_information.alternative_communication AS helper_alternative_communication,
    helper_information.phone_number AS helper_phone_number,
    helper_information.user_location AS helper_location
FROM relevant_jobs
LEFT JOIN relevant_pictures ON
    relevant_jobs.job_id = relevant_pictures.job_id
JOIN relevant_labels ON
    relevant_jobs.job_id = relevant_labels.job_id
JOIN owners ON
    relevant_jobs.job_id = owners.job_id
JOIN helper_information ON
    helper_information.job_id = relevant_jobs.job_id
ORDER BY
    helper_information.datetime_confirmation_utc
;
    