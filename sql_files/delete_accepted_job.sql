WITH job_id AS (
    SELECT
        jobs.job_id
    FROM jobs
    WHERE
        jobs.title = {title}
)
DELETE FROM users_completed_jobs
WHERE
    users_completed_jobs.user_id = {user_id}
    AND users_completed_jobs.job_id = job_id.job_id