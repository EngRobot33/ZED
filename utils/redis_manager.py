
from redis import StrictRedis

class RedisHandler:

    def __init__(self,redis_host:str,redis_port:int,redis_db:int = 0) -> None:
        
        self.__redis_host:str = redis_host
        self.__redis_port:int = redis_port
        self.__redis_db = redis_db

        self.__redis_client = None

    def connect(self):

        self.__redis_client = StrictRedis(host=self.__redis_host,port=self.__redis_port,db=self.__redis_db)

    @property
    def redis_client(self) -> StrictRedis:
        return self.__redis_client