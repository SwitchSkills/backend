SELECT
    label_name
FROM user_has_labeled_skills
WHERE
    user_has_labeled_skills.user_id = {user_id}