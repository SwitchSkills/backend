UPDATE users
SET users.first_name ={new_first_name} , users.last_name = {new_last_name}
WHERE users.user_id = {existing_user_id}