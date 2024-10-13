class HTTPError(Exception):
    """Класс исключений при HTTP ошибках"""
    def __init__(self, *args):
        self.status = args[0] if args else None
        self.message = args[1] if args else None
    
    def __str__(self):
        return f"Ошибка: {self.message}, Статус - код: {self.status}"