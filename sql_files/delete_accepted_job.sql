
DELETE FROM users_completed_jobs
WHERE
    users_completed_jobs.user_id = {user_id}
    AND users_completed_jobs.job_id = {job_id}
    AND users_completed_jobs.pending