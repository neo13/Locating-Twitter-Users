import redis
class GeoNamesCanada:
    server = 'localhost'
    port = 6379
    db = 0
    r = redis.StrictRedis(host=server, port=port, db=db)

    @classmethod
    def lookup(cls, name):
        key = cls.r.keys(name)
        if len(key):
            return True
        else:
            return False
