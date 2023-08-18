SELECT
    users.rating,
    users.number_of_ratings
FROM users
WHERE users.user_id ={user_id}