
def check_len(password):
    if 12 <= len(password) <= 16:
        return True
    else:
        return False
def check_numbers(password):
    if password.isalpha() == False:
        return True
    else:
        return False
def check_upper_lower(password):
    if password.upper() != password and password.lower() != password:
        return True
    else:
        return False
def check_other_symbols(password):
    for i in password:
        if i not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_':
            return False
    return True



