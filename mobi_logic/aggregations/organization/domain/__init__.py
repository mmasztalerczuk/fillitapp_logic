
subscribers = {}


def publish(event):
    if type(event) in subscribers:
        for handler in subscribers[type(event)]:
            handler(event)


def subscribe(event_type, handler):
    if event_type in subscribers:
        subscribers[event_type].append(handler)
    else:
        subscribers[event_type] = [handler]
