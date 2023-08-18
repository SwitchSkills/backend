WITH job_id AS (
    SELECT
        jobs.job_id
    FROM jobs
    WHERE
        jobs.title = {title}
)
DELETE FROM users_like_jobs
WHERE
    users_like_jobs.user_id = {user_id}
    AND users_like_jobs.job_id = job_id.job_id