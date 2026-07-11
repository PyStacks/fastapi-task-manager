from passlib.context import CryptContext

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    :param plain_password:
    :param hashed_password:
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    生成哈希密码
    :param password:
    :return:
    """
    return pwd_context.hash(password)


if __name__ == '__main__':
    password = '123qwe'
    password1 = '123345333we'
    hashed_password = get_password_hash(password)
    print(hashed_password)
    print(verify_password(password, hashed_password))
    print(verify_password(password1,hashed_password))