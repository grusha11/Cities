
database = {'A': '123412341234Af'}

def db_check_pasw(login, password: object) -> object:
    if login not in database:
        database[login] = password
        print(database)


