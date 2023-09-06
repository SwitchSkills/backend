import hashlib
import uuid

from codebase_backend.SingletonMeta import SingletonMeta


class CredentialsFactory(metaclass=SingletonMeta):

    __namespace_user = uuid.UUID('b34ed496-5c86-4228-a190-278c71b44f00')
    __namespace_job = uuid.UUID('9520da0e-1d40-4ffe-8422-40d0ab16acaf')
    __namespace_region = uuid.UUID('3cc7b667-7157-427f-abfb-89a27323e8b5')
    __namespace_picture = uuid.UUID('0b2552b9-6d03-4712-9c69-e6c558a9a386')

    def __int__(self):
        pass

    @staticmethod
    def hash_string(str_tohash:str) -> str:
        return hashlib.sha3_512(str_tohash.encode("utf-8")).hexdigest()

    def get_user_id(self, first_name:str, last_name:str)->str:
        return str(uuid.uuid5(self.__namespace_user, first_name+last_name))

    def get_picture_id(self, location:str) ->str:
        return str(uuid.uuid5(self.__namespace_picture, location))

    def get_job_id(self, job_title:str, user_id_owner:str, region_id:str) ->str:
        return str(uuid.uuid5(self.__namespace_job, job_title+user_id_owner+region_id))

    def get_region_id(self,country, region_name):
        return str(uuid.uuid5(self.__namespace_region, country+region_name))
