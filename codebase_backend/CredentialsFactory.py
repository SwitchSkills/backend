import hashlib
import uuid


class CredentialsFactory:

    __namespace_user = uuid.UUID('b34ed496-5c86-4228-a190-278c71b44f00')
    __namespace_job = uuid.UUID('9520da0e-1d40-4ffe-8422-40d0ab16acaf')
    __namespace_region = uuid.UUID('3cc7b667-7157-427f-abfb-89a27323e8b5')
    def __int__(self):
        pass

    @staticmethod
    def hash_string(str_tohash):
        return hashlib.sha3_512(str_tohash.encode("utf-8")).hexdigest()

    def get_user_id(self, first_name, second_name):
        return uuid.uuid5(self.__namespace_user, first_name+second_name)

    def get_picture_id(self):
        return uuid.uuid4()

    def get_job_id(self, job_title, user_id_owner, region_id):
        return uuid.uuid5(self.__namespace_job, job_title+user_id_owner+region_id)

    def get_region_id(self,country, region_name):
        return uuid.uuid5(self.__namespace_region, country+region_name)
