import json
import subprocess
import threading
import time
from pathlib import Path


from database import save_service
from models import ServiceStatus


def update_all_services_status(services_filepath: Path):
    """Runs check script and update all services status.

    Raises:
        IOError: When the give services file does not exist.
    """
    if isinstance(services_filepath, str):
        services_filepath = Path(services_filepath)

    if not services_filepath.exists():
        raise IOError('Services file does not exist')

    with open(services_filepath, encoding='utf-8') as file:
        services = json.load(file)
        for service in services:
            update_service_status(service)


def initialize_check_schedulers(services_filepath: Path, default_interval: int):
    """Initialize schedulers for each service based on give services file content.

    Raises:
        IOError: When the give services file does not exist.
    """
    if isinstance(services_filepath, str):
        services_filepath = Path(services_filepath)

    if not services_filepath.exists():
        raise IOError('Services file does not exist')

    with open(services_filepath, encoding='utf-8') as file:
        services = json.load(file)
        for service in services:
            check_interval = service.get('check-interval') or default_interval
            schedule_task(check_interval, update_service_status,
                          service)


def update_service_status(service):
    """Runs the check script and update the status on the database.

        Raises:
            TypeError: When a service has invalid format.
            IOError: When a services check script file does not exist.
            ValueError: When script output is invalid.

        Returns: ServiceStatus 
    """
    label = service['label']
    check_script_filepath = service['check-script']

    if not Path(check_script_filepath).exists():
        raise IOError(f'{check_script_filepath} file does not exist')

    status: ServiceStatus = subprocess.check_output(
        ['bash', check_script_filepath]).decode('utf-8').strip().splitlines()[-1]

    save_service(label, status)


def schedule_task(interval: float, task, *args):
    """
    Runs the given function in loop and waits
    [interval] seconds between each execution.
    """
    def task_wrapper():
        while True:
            task(*args)
            time.sleep(interval)

    thread = threading.Thread(target=task_wrapper)
    thread.daemon = True
    thread.start()
