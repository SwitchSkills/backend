UPDATE jobs
SET jobs.title ={new_title}, jobs.job_id = {new_job_id}
WHERE jobs.job_id = {existing_job_id}