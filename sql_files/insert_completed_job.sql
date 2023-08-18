WITH job_id AS (
    SELECT
        jobs.job_id
    FROM jobs
    WHERE
        jobs.title = {title}
)
UPDATE users_completed_jobs
SET users_completed_jobs.pending = FALSE {datetime_confirmation_utc_key} {datetime_confirmation_utc_content}
WHERE
    user_id = {user_id}
    AND job_id = job_id.job_id