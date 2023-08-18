SELECT
    region_name,
    country
FROM region
WHERE
    region_id IN {region_id_list}