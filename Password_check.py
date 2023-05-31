
class PasswordCheck(object):

    def __init__(self, password):
        if self.check_len(password) and self.check_numbers(password) and self.check_upper_lower(password) and self.check_other_symbols(password):
            self.password = password

    @classmethod
    def check_len(cls, password):
        if 12 <= len(password) <= 16:
            return True
        else:
            return False

    @classmethod
    def check_numbers(cls, password):
        if password.isalpha() == False:
            return True
        else:
            return False

    @classmethod
    def check_upper_lower(cls, password):
        if password.upper() != password and password.lower() != password:
            return True
        else:
            return False

    @classmethod
    def check_other_symbols(cls, password):
        for i in password:
            if i not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_':
                return False
        return True



# p = PasswordCheck(input('Введите пароль: '))
# print(p.__dict__)

