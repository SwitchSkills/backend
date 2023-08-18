INSERT INTO picture(
        picture_id,
        picture_location_firebase,
        {description_key},
        {user_id_key},
        {job_id_key}
)
VALUES({picture_id},
        {picture_location_firebase},
          {description_content},
          {user_id_content},
          {job_id_content}
      );