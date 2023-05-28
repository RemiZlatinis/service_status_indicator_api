import sqlite3

from src.logger import log, error
from src.models import ServiceStatus

DATABASE_FILENAME = "data.db"

# Initialize the database
try:
    _conn = sqlite3.connect(DATABASE_FILENAME)
    _c = _conn.cursor()
    _c.execute("""CREATE TABLE services (label text, status text)""")
    _conn.commit()
    _conn.close()
    log("Database initlilized")
except sqlite3.OperationalError as e:
    error(f"Error on database initialize: {e}")


def get_services() -> dict[str, ServiceStatus] | None:
    """
    Returns the latest status of services.

    Raises:
        OperationalError: When database is unreachable.

    Returns: A dictionary that contains key-value pairs of services label and status.
    `Example: {'service_1': 'ok', 'service_2': 'update'}`
    """
    with sqlite3.connect(DATABASE_FILENAME) as conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT label, status FROM services")
            rows = cursor.fetchall()

            services: dict[str, ServiceStatus] = {}
            for row in rows:
                label, status = row
                services[label] = status

            return services
        except sqlite3.OperationalError as err:
            error(f"Error on getting services: {err}")


def save_service(label: str, status: ServiceStatus):
    """
    Saves the given key-value pair on services table.

    Params:
        `label`: str
        `status`: ServiceStatus

    Raises:
        OperationalError: When database is unreachable.
    """
    with sqlite3.connect(DATABASE_FILENAME) as conn:
        try:
            conn.execute(
                "INSERT INTO services(label, status) VALUES(?, ?)", (label, status)
            )
            conn.commit()
        except sqlite3.OperationalError as err:
            error(f"Error on saving service: {err}")
