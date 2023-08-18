UPDATE jobs
SET jobs.title ={new_title}
WHERE jobs.job_id = {existing_job_id}