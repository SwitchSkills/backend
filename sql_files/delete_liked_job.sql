
DELETE FROM users_like_jobs
WHERE
    users_like_jobs.user_id = {user_id}
    AND users_like_jobs.job_id = {job_id}