import random as rand
import string


class RobloxAccount:
    def __init__(self, month: int = 1, day: int = 1, year: int = 1999, username: str = None, password: str = None, gender: int = 1):
        self._month = month
        self._day = day
        self._year = year
        self._username = username
        self._password = password
        self._gender = gender

    @property
    def month(self) -> str:
        data = {
            1: 'Jan',
            2: 'Feb',
            3: 'Mar',
            4: 'Apr',
            5: 'May',
            6: 'Jun',
            7: 'Jul',
            8: 'Aug',
            9: 'Sep',
            10: 'Oct',
            11: 'Nov',
            12: 'Dec'
        }

        return data[self._month]

    @property
    def day(self) -> str:
        return str(self._day).zfill(2)

    @property
    def year(self) -> int:
        return self._year

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    @property
    def gender(self) -> int:
        return self._gender


def rand_username() -> str:
    k = rand.randint(6, 9)
    return ''.join(rand.choices(string.ascii_lowercase, k=k))


def ran_password() -> str:
    number = rand.randint(100000000, 900000000)
    char = rand.choice(string.ascii_uppercase)

    number = str(number)

    return f'{number}{char}'


def rand_account() -> RobloxAccount:
    month = rand.randint(1, 12)
    day = rand.randint(1, 28)
    year = rand.randint(2000, 2011)
    username = rand_username()
    password = ran_password()
    gender = rand.randint(1, 2)

    return RobloxAccount(month, day, year, username, password, gender)
