from services.connection_manager import ConnectionManager

connection_manager = ConnectionManager()


def get_connection_manager():
    return connection_manager
