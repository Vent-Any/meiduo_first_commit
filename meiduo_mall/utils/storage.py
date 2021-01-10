from django.core.files.storage import Storage


class QiniuStorage(Storage):
    # 存储类必须声明_open方法
    def _open(self, name, mode='rb'):
        pass

    def _save(self, name, content, max_length=None):
        pass

    def url(self, name):
        return 'http://qmllvum7m.hn-bkt.clouddn.com/'+ name

