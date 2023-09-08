relevant_pictures AS (
SELECT DISTINCT
    relevant_users.user_id,
    picture.picture_location_firebase,
    picture.description AS picture_description
FROM picture
JOIN relevant_users ON
    relevant_users.user_id = picture.user_id
    ),
relevant_labels AS (
SELECT DISTINCT
    relevant_users.user_id,
    labels.label_name,
    labels.description AS label_description
FROM labels
JOIN user_has_labeled_skills ON
    user_has_labeled_skills.label_name = labels.label_name
JOIN relevant_users ON
    relevant_users.user_id = user_has_labeled_skills.user_id
)

