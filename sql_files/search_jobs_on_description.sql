WITH relevant_regions AS (
SELECT
    region_id,
    region_name,
    country
FROM region
WHERE
    region_id IN {region_id_list}
),
{completed_jobs},
{accepted_jobs},
relevant_jobs AS (
SELECT
    jobs.job_id,
    jobs.description AS job_description,
    jobs.title,
    relevant_regions.region_name,
    relevant_regions.country,
    jobs.user_id_owner,
    jobs.datetime_made_utc,
    jobs.location AS job_location
FROM jobs
JOIN relevant_regions ON
    jobs.region_id = relevant_regions.region_id
WHERE
    jobs.job_id NOT IN (SELECT job_id FROM completed_jobs)
    AND jobs.job_id NOT IN (SELECT job_id FROM accepted_jobs)
    AND jobs.description LIKE '%{search}%'
),
{job_additional_information}
SELECT
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
JOIN relevant_labels ON
    relevant_jobs.job_id = relevant_labels.job_id
JOIN owners ON
    relevant_jobs.job_id = owners.job_id
ORDER BY
    relevant_jobs.datetime_made_utc
;
