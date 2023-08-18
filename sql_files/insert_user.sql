INSERT INTO users(  user_id,
                    first_name,
                    last_name,
                    email_address ,
                    phone_number,
                    password,
                    location,
                    {alternative_communication_key},
                    {bibliography_key},
                    {rating_key},
                    {number_of_ratings_key})
VALUES
    ( {user_id},
        {first_name},
        {last_name},
        {email_address},
        {phone_number},
        {password},
        {location},
        {alternative_communication_content},
        {bibliography_content},
        {rating_content},
        {number_of_ratings_key_content}
     );