from secrets import compare_digest

# I know it's dumb, but im too lazy for now to implement any kind of DB. I's gonna be done later :)
users = [
    {
        'id': 1,
        'username': 'admin',
        'password': 'password',
    },
]


class User:
    def __init__(self, data: dict):
        self.id: int = data['id']
        self.username: str = data['username']
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self) -> str:
        return str(self.id)

    @classmethod
    def get(cls, user_id: str | int):
        try:
            return User([data for data in users if data['id'] == int(user_id)][0])
        except IndexError:
            return None

    @classmethod
    def get_by_login_and_password(cls, username: str, password: str):
        try:
            return User([
                data for data in users
                if data['username'] == username and compare_digest(data['password'], password)
            ][0])
        except IndexError:
            return None
