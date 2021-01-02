class UsernameConverter:
    regex = '[a-zA-Z0-9_-]{5,20}'

    def to_python(self, value):
        return str(value)


class MobileConverter:
    regex = '1[3-9]\d{9}'

    def to_python(self, value):
        print(value)
        return str(value)
