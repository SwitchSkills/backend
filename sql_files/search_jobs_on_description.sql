WITH relevant_regions AS (
SELECT
    region_id,
    region_name,
    country
FROM region
WHERE
    country = {country}
    AND region_name IN {region_name_list}
),
{completed_jobs},
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
JOIN relevant_regions ON
    jobs.region_id = region.region_id
    AND jobs.job_id NOT IN completed_jobs.job_id
    AND jobs.description LIKE '%{search_description}%'
),
{job_additional_information}
SELECT
    relevant_jobs.datetime_made_utc AS datetime_utc,
    relevant_jobs.title,
    relevant_jobs.job_description,
    relevant_jobs.job_location,
    relevant_jobs.region,
    relevant_jobs.country,
    pictures.picture_data,
    pictures.picture_description,
    labels.label_name,
    labels.label_description,
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
