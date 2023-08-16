relevant_pictures_users AS (
SELECT
    relevant_user_ids.user_id,
    picture.picture_data,
    picture.description AS picture_description
FROM picture
JOIN relevant_users ON
    relevant_users.user_id = picture.user_id
    )