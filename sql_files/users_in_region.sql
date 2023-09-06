WITH relevant_regions AS (
    SELECT
        region_name,
        region_id,
        country
    FROM region
    WHERE
        region_id IN {region_id_list}
),
relevant_users AS (
SELECT
    user_is_active_in_region.user_id,
    relevant_regions.region_name,
    relevant_regions.country
FROM relevant_regions
JOIN user_is_active_in_region ON
    user_is_active_in_region.region_id = relevant_regions.region_id
    ),
{user_additional_information}

SELECT
    users.user_id,
    users.first_name,
    users.last_name,
    users.email_address,
    users.phone_number,
    users.alternative_communication,
    users.bibliography,
    users.location,
    relevant_users.country,
    relevant_users.region_name,
    relevant_pictures.picture_location_firebase,
    relevant_pictures.picture_description,
    relevant_labels.label_name,
    relevant_labels.label_description
FROM users
JOIN relevant_users ON
    users.user_id = relevant_users.user_id
LEFT JOIN relevant_pictures ON
    users.user_id = relevant_pictures.user_id
LEFT JOIN relevant_labels ON
    users.user_id = relevant_labels.user_id
