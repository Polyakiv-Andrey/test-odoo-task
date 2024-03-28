from datetime import datetime


def upload_to(instance, filename):
    now = datetime.now().strftime('%Y/%m/%d/%H-%M-%S')
    return f'files/{now}/{filename}'
