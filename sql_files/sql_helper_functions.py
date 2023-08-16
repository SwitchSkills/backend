
def read_sql_file(filename:str,sub_query: bool = False) -> str:
    if sub_query:
        with open('sql_files/'
                  'sub_query/'
                  f'{filename}.sql','r') as file:
            return file.read()

    else:
        with open('sql_files/'
                  f'{filename}.sql','r') as file:
            return file.read()