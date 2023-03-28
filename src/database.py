import sqlite3

from logger import log, error
from models import ServiceStatus

DATABASE_FILENAME = 'data.db'

# Initialize the database
try:
    _conn = sqlite3.connect(DATABASE_FILENAME)
    _c = _conn.cursor()
    _c.execute('''CREATE TABLE services (label text, status text)''')
    _conn.commit()
    _conn.close()
    log('Database initlilized')
except sqlite3.OperationalError as e:
    error(f'Error on database initialize: {e}')


def get_services() -> dict[str, str]:
    """
    Returns the latest status of services.

    Raises:
        OperationalError: When database is unreachable.

    Returns: A dictionary that contains key-value pairs of services label and status.
    `Example: {'service_1': 'ok', 'service_2': 'update'}`
    """
    try:
        conn = sqlite3.connect(DATABASE_FILENAME)
        cursor = conn.cursor()
        cursor.execute('SELECT label, status FROM services')
        rows = cursor.fetchall()

        services = {}
        for row in rows:
            label, status = row
            services[label] = status

        conn.close()
        return services
    except sqlite3.OperationalError as error:
        error(f'Error on getting services: {error}')


def save_service(label: str, status: ServiceStatus):
    """
    Saves the given key-value pair on services table.

    Params:
        `label`: str
        `status`: ServiceStatus

    Raises:
        OperationalError: When database is unreachable.
    """
    # cursor = conn.cursor()
    # cursor.execute("DELETE FROM services')
    try:
        conn = sqlite3.connect(DATABASE_FILENAME)
        conn.execute(
            'INSERT INTO services(label, status) VALUES(?, ?)', (label, status))
        conn.commit()
    except sqlite3.OperationalError as error:
        error(f'Error on saving service: {error}')
    finally:
        conn.close()
