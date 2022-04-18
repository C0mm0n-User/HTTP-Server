class Request:
    def __init__(self, method, target, version, headers, rfile):
        self.method = method # Метод запроса
        self.target = target # Цель запроса
        self.version = version # Версия протокола HTTP
        self.headers = headers # Заголовки запроса
        self.rfile = rfile # "Переменная" запроса
