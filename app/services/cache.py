# import redis
# from app.core.config import get_settings
#
# _settings = get_settings()
#
# def get_redis():
#     return redis.Redis(host=_settings.REDIS_HOST, port=_settings.REDIS_PORT, db=_settings.REDIS_DB)
#
# def ping_redis() -> bool:
#     try:
#         r = get_redis()
#         return r.ping()
#     except Exception:
#         return False
