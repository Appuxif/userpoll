import sys
import time

from django.db.utils import OperationalError
import manage

sys.argv.append('makemigrations')

timer = time.monotonic()
while time.monotonic() - timer < 120:
    try:
        manage.main()
    except OperationalError as err:
        time.sleep(10)
    else:
        break
