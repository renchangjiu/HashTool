import hashlib


class HashUtil(object):
    @staticmethod
    def MD5(file_path: str) -> str:
        md5 = hashlib.md5()
        file = open(file_path, "rb")
        while True:
            r = file.read(1024 * 8)
            if not r:
                md5.update(r)
            else:
                break
        file.close()
        return md5.hexdigest()

    @staticmethod
    def SHA1(file_path: str) -> str:
        sha1 = hashlib.sha1()
        file = open(file_path, "rb")
        while True:
            r = file.read(1024 * 8)
            if not r:
                sha1.update(r)
            else:
                break
        file.close()
        return sha1.hexdigest()

    @staticmethod
    def SHA256(file_path: str) -> str:
        sha256 = hashlib.sha256()
        file = open(file_path, "rb")
        while True:
            r = file.read(1024 * 8)
            if not r:
                sha256.update(r)
            else:
                break
        file.close()
        return sha256.hexdigest()
