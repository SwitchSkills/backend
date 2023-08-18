WITH job_id AS (
    SELECT
        jobs.job_id
    FROM jobs
    WHERE
        jobs.title = {title}
)
INSERT INTO users_like_jobs (user_id,job_id)
VALUES (
        {user_id},
        job_id.job_id
        );