completed_jobs AS (
SELECT
    job_id,
    user_id,
    datetime_confirmation_utc
FROM users_completed_jobs
WHERE
    pending IS FALSE
    )