import json
import subprocess
import threading
import time
import typing
from pathlib import Path


from database import save_service
from logger import log
from models import ServiceStatus


def initialize_check_schedulers(services_filepath: Path, default_interval: int):
    """Initialize schedulers for each service based on give services file content.

    Raises:
        IOError: When the give services file does not exist.
    """
    if isinstance(services_filepath, str):
        services_filepath = Path(services_filepath)

    if not services_filepath.exists():
        raise IOError("Services file does not exist")

    with open(services_filepath, encoding="utf-8") as file:
        services = json.load(file)
        for service in services:
            check_interval = service.get("check-interval") or default_interval
            schedule_task(check_interval, update_service_status, service)


def update_service_status(service):
    """Runs the check script and update the status on the database.

    Raises:
        TypeError: When a service has invalid format.
        IOError: When a services check script file does not exist.
        ValueError: When script output is invalid.

    Returns: ServiceStatus
    """
    log(f"Updating {service['label']}")
    label = service['label']
    check_script_filepath = service['check-script']

    if not Path(check_script_filepath).exists():
        raise IOError(f"{check_script_filepath} file does not exist")

    try:
        result = subprocess.run(['bash', check_script_filepath],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        status = result.stdout.decode('utf-8').strip().splitlines()[-1]
    except subprocess.CalledProcessError as error:
        status = f"ERROR: {error.stderr.decode('utf-8').strip()}"

    if status in typing.get_args(ServiceStatus):
        save_service(label, status)  # type: ignore
    else:
        log(f'Service "{label}" return invalid status of "{status}"')


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
