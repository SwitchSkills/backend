UPDATE jobs
SET jobs.region_id ={new_region_id}, jobs.job_id = {new_job_id}
WHERE jobs.job_id = {existing_job_id}