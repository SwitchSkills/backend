INSERT INTO users(  user_id,
                    first_name,
                    last_name,
                    email_address ,
                    phone_number,
                    alternative_communication,
                    bibliography ,
                    password,
                    location,
                    rating,
                    number_of_ratings)
VALUES
    ( '77a0a019-5488-5d10-8b96-dee54a414961',
     'Nation',
     'Builder',
     'nation.builder.team@gmail.com',
     '+919216753560',
     'https://www.linkedin.com/in/tristan-toye-7a8515229/',
     'passionate and engaged team',
     'bf7f37d0a553d4ef30fa2ee62be0cbbac95869dcbf84ef72a8194b1a725fc84ddb568be9d3bcdd98db78fa4e2a28d4bf54248b24d60f64683e6dd08826005fd9',#NationBuilders
     'Washington D.C.',
     5,
     100
     );

INSERT INTO users(  user_id,
                    first_name,
                    last_name,
                    email_address ,
                    phone_number,
                    alternative_communication,
                    bibliography ,
                    password,
                    location)
VALUES
    ( 'c71ae733-baaa-52a0-899a-5c344e4160b7',
     'Tristan',
     'Toye',
     'tistan.toye@outlook.com',
     '+32476267397',
     'https://www.linkedin.com/in/tristan-toye-7a8515229/',
     'passionate computer science student',
    '8b3ff73da5744132bbdae70002bfdec7e9003a21fdfbfdb27aa6ce5891824ff633500049bfa41cf64510f61d6a7748dcaa2ce7b121c12139a01fa8f03c163349', #TristanToye
    'MUJ, Jaipur, Rajasthan, India'
     );

INSERT INTO users(  user_id,
                    first_name,
                    last_name,
                    email_address ,
                    phone_number,
                    bibliography ,
                    password,
                    location)
VALUES
    ('376caee5-5ae7-5967-90a1-b7eb3afc310f',
     'Dag',
     'Malstaf',
     'dag.malstaf@gmail.com',
     '+32471785072',
     'passionate computer science student 2.0',
     'b4b4f8c0f8f5344fac1355622b52ec2c722220bd0f44bce2ce334b7a618e9276bd7582d85c4d15e3e4bf809cee9ab51d46d2b7ac4bc4773b98894a3a940805b5',#DagMalstaf
     'Leuven, Belgium'
    );

INSERT INTO users(  user_id,
                    first_name,
                    last_name,
                    email_address ,
                    phone_number,
                    password,
                    location)
VALUES
    ('baf6a8a6-0dae-53ac-a75e-0f7e5499cf74',
     'Judith',
     'Van Looveren',
     'judithvanlooveren1@gmail.com',
     '+32470131500',
    '911f1ead422f7603a77b8c5f6b4a58ad39a309f8883af48f42acac81351d0b4143a5fe6f6ed7158f091b2d9669d1727683a758873f8dea71d4760e42be70451d',#JVL
    'Ecuador'
   );

INSERT INTO picture(
        picture_id,
        picture_location_firebase,
        description,
        user_id
)
VALUES(
       '17b9cfc4-2c1d-4b75-a98d-b4e041abf0d4',
       'gs://switchskills-1c163.appspot.com/Brussels/Nation_builder_image_dummy_data.png',
       'Logo US state department',
       '77a0a019-5488-5d10-8b96-dee54a414961'
      );

UPDATE users
SET picture_id = '17b9cfc4-2c1d-4b75-a98d-b4e041abf0d4'
WHERE user_id = '77a0a019-5488-5d10-8b96-dee54a414961';


INSERT INTO region(region_id,region_name,country)
VALUES(
        '42f61a13-ef12-57a2-92af-ae659dd39e83',
       'West Flanders',
       'Belgium'
      ),
    (
        '52481fe7-1188-5df1-8444-2cbab6c77b79',
       'Antwerp',
       'Belgium'
      ),
    (
        'fca79e85-4742-5e65-858b-a0a0f31c7565',
       'East Flanders',
       'Belgium'
      ),(
        '5472faf9-debe-512c-b236-ba9f6593b2b2',
       'Flemish Brabant',
       'Belgium'
      ),(
        '6e939872-fb10-5d0f-9758-bd9b30c8d360',
       'Limburg',
       'Belgium'
      ),(
        'be4caf9c-93c4-5d4c-9f44-1e559a347ba4',
       'Hainaut',
       'Belgium'
      ),(
        '9cc519b0-4678-5996-9d04-e5fcbbe6f003',
       'Liège',
       'Belgium'
      ),(
        'f6c8aec7-242a-5536-8bb4-494093373517',
       'Luxembourg',
       'Belgium'
      ),(
        'beba740f-7f9b-5757-93d5-a200403185d5',
       'Namur',
       'Belgium'
      ),(
        '8dc2090c-b309-56fd-b783-128591000997',
       'Walloon Brabant',
       'Belgium'
      ),(
        '5e01c8b7-4405-5ffb-886d-1870bdf3ec44',
       'Brussels Capital Region',
       'Belgium'
      );

INSERT INTO labels(label_name,description)
VALUES
    ('bicycle repair', 'mechanical repair for non-electric bicycles');

INSERT INTO jobs(
                 job_id,
                 description,
                 title,
                 region_id,
                 user_id_owner,
                 location
)VALUES(
        'df4990ec-b597-54eb-a3cd-2f19d7019bfd',#get_job_id('repair of bike','77a0a019-5488-5d10-8b96-dee54a414961','5e01c8b7-4405-5ffb-886d-1870bdf3ec44') (Nation Builder, Brussels
        'Need someone to repair a flat tire. I have no equipment at all, not even a pump , nor any spare tires.',
        'repair of bike',
        '5e01c8b7-4405-5ffb-886d-1870bdf3ec44',
        '77a0a019-5488-5d10-8b96-dee54a414961',
        'VUB campus, Brussels'
       );

INSERT INTO user_is_active_in_region(
                                     user_id,
                                     region_id
)
VALUES('77a0a019-5488-5d10-8b96-dee54a414961','5e01c8b7-4405-5ffb-886d-1870bdf3ec44'),
      ('77a0a019-5488-5d10-8b96-dee54a414961','f6c8aec7-242a-5536-8bb4-494093373517'),
      ('c71ae733-baaa-52a0-899a-5c344e4160b7', '42f61a13-ef12-57a2-92af-ae659dd39e83'),
      ('baf6a8a6-0dae-53ac-a75e-0f7e5499cf74','5e01c8b7-4405-5ffb-886d-1870bdf3ec44');

INSERT INTO job_needs_labeled_skills(
                                     job_id,
                                     label_name
)VALUES
     (
        'df4990ec-b597-54eb-a3cd-2f19d7019bfd',
      'bicycle repair'
     );

INSERT INTO users_like_jobs(
                            user_id,
                            job_id
) VALUES(
         'baf6a8a6-0dae-53ac-a75e-0f7e5499cf74',
         'df4990ec-b597-54eb-a3cd-2f19d7019bfd'
        );