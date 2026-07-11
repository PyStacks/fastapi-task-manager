from datetime import datetime, timezone

# 获取当前UTC时间
def utc_now() -> datetime:
    return datetime.now(timezone.utc)
