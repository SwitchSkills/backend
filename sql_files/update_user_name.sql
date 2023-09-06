UPDATE users
SET users.first_name ={new_first_name} , users.last_name = {new_last_name}, users.user_id = {new_user_id}
WHERE users.user_id = {existing_user_id}