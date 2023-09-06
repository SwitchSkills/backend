{users_in_region}
WHERE
    users.first_name LIKE '%{search_first_name}%'
    AND users.last_name LIKE '%{search_last_name}%'
