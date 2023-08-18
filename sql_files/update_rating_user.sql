UPDATE users
SET users.rating = {rating}, users.number_of_ratings = {number_of_ratings}
WHERE
    users.user_id = {user_id}