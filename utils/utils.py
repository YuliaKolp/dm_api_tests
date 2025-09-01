import random, string


def generate_random_string(
        str_length=5
        ) -> str:
    chars = string.ascii_letters + string.digits + '!@#$%^&*'
    return ''.join(random.choices(chars, k=str_length))


def generate_login() -> str:
    prefix = 'yk_test'
    postfix_length = 5
    postfix = generate_random_string(postfix_length)
    login = f'{prefix}_{postfix}'
    return login
