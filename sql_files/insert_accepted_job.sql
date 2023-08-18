WITH job_id AS (
    SELECT
        jobs.job_id
    FROM jobs
    WHERE
        jobs.title = {title}
)
INSERT INTO users_completed_jobs(user_id,
                                 job_id,
                                 pending,
                                {datetime_request_utc_key})
VALUES (
           {user_id},
            job_id.job_id,
           {pending},
           {datetime_request_utc_content}
       )