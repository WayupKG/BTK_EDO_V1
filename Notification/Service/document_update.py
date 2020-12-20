from Documents.models import Document

import time
import threading


def update():
    doc = Document.objects.filter(status='В процессе')
    print(doc)


while True:
    time.sleep(3)
    thread = threading.Thread(target=update)
    thread.start()

