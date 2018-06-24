from mobi_logic import event_queue


def publish(event):
    event_queue.append(event)


