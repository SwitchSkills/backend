import threading

user_lock = threading.Semaphore(1)
picture_lock = threading.Semaphore(1)
label_user_lock = threading.Semaphore(1)
label_job_lock = threading.Semaphore(1)
region_lock = threading.Semaphore(1)
job_lock = threading.Semaphore(1)