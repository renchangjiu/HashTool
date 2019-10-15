import hashlib


class HashUtil(object):

    @staticmethod
    def MD5(file_path: str) -> str:
        md5 = hashlib.md5()
        return HashUtil.file_hash(md5, file_path)

    @staticmethod
    def SHA1(file_path: str) -> str:
        sha1 = hashlib.sha1()
        return HashUtil.file_hash(sha1, file_path)

    @staticmethod
    def SHA256(file_path: str) -> str:
        sha256 = hashlib.sha256()
        return HashUtil.file_hash(sha256, file_path)

    @staticmethod
    def file_hash(hash_obj, file_path: str) -> str:
        file = open(file_path, "rb")
        while True:
            r = file.read(1024 * 8)
            if len(r) != 0:
                hash_obj.update(r)
            else:
                break
        file.close()
        return hash_obj.hexdigest().upper()

    @staticmethod
    def string_hash(hash_alg: str, string: str) -> str:
        hash_obj = None
        if hash_alg.upper() == "MD5":
            hash_obj = hashlib.md5()
        elif hash_alg.upper() == "SHA1":
            hash_obj = hashlib.sha1()
        elif hash_alg.upper() == "SHA256":
            hash_obj = hashlib.sha256()
        else:
            return ""
        hash_obj.update(string.encode())
        return hash_obj.hexdigest().upper()
