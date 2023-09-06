
INSERT INTO users_completed_jobs(user_id,
                                 job_id,
                                 pending
                                {datetime_request_utc_key})
VALUES (
           {user_id},
           {job_id},
           {pending}
           {datetime_request_utc_content}
       )