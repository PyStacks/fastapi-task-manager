import hmac
import hashlib
import base64
import json

def base64url_encode(data:bytes) -> str:
    """JWT专用的Base64URL编码（去掉=，+变-，/变_）"""
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def base64url_decode(data:str) -> bytes:
    """JWT专用解码"""
    padding = 4 - len(data) % 4
    if padding != 4:
        data += '=' * padding
    return base64.urlsafe_b64decode(data)

def create_token(payload: dict, secret: str) -> str:
    """手动创建一个JWT"""
    header = {"alg": "HS256", "typ": "JWT"}

    header_b64 = base64url_encode(json.dumps(header).encode())
    payload_b64 = base64url_encode(json.dumps(payload).encode())

    message = f"{header_b64}.{payload_b64}".encode()
    signature  = hmac.new(secret.encode(), message, hashlib.sha256).digest()

    signature_b64 = base64url_encode(signature)

    return f"{header_b64}.{payload_b64}.{signature_b64}"

def verify_token(token: str, secret: str) -> dict:
    """手动验证JWT"""
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("无效的Token格式")

    header_b64, payload_b64, signature_b64 = parts
    message = f"{header_b64}.{payload_b64}".encode()
    expected_signature = hmac.new(secret.encode(), message, hashlib.sha256).digest()
    expected_b64 = base64url_encode(expected_signature)

    if not hmac.compare_digest(signature_b64, expected_b64):
        raise ValueError("签名验证失败")

    return json.loads(base64url_decode(payload_b64))


# 测试
if __name__ == "__main__":
    header = {"alg1": "HS256", "typ": "JWT"}
    data = json.dumps(header).encode()
    print(len(data))
    print(base64.urlsafe_b64encode(data).decode())

    # secret = "my-secret-key"
    # token = create_token({"user_id": 123, "exp": 1700000000}, secret)
    # print(f"生成的Token: {token}")
    #
    # payload = verify_token(token, secret)
    # print(f"解析出的Payload: {payload}")