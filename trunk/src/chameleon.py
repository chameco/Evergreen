#Copyright 2011 Samuel Breese, alias chameco.
"""
A simple framework for managing events.
"""
class event():
    __slots__ = ["name", "data"]
    """
    An event. Pass one to an eventManager's alert method to
    notify all registered eventListeners set to the event's name
    of its occurance.
    """
    def __init__(self, name, data):
        self.name = name
        self.data = data
class manager():
    __slots__ = ["listeners"]
    """
    Manages events and eventListeners. To use, register an eventListener
    using register(), then call alert() as needed. The "primary" listener
    should be in slot 0. This only matters when using prireg(). *ONLY* register
    non-blocking functions. Every time an eventManager blocks a kitten dies.
    """
    def __init__(self):
        self.listeners = {}
    def alert(self, event):
        """
        Alert all registered listeners of an event.
        """
        if event.name in self.listeners:
            for listener in self.listeners[event.name]:
                listener._alert(event)
    def reg(self, eventName, listener):
        """
        Register a listener to the eventManager.
        """
        listener.eventManager = self
        if eventName in self.listeners.keys():
            self.listeners[eventName].append(listener)
        else:
            self.listeners[eventName] = [listener]
    def unregister(self, eventName, listener):
        self.listeners[eventName].remove(listener)
class listener():
    __slots__ = ["responses", "eventmanager"]
    """
    Responds to events.
    """
    def __init__(self):
        self.responses = {}
        self.eventManager = None
    def _alert(self, event):
        """
        Call the set response to an event. The event's
        data attribute is passed to the response function.
        """
        if event.name in self.responses.keys():
            self.responses[event.name](event.data)
    def setResponse(self, eventName, response):
        """
        Set a response to an event. The response must take one
        argument, used for the event's data.
        """
        self.responses[eventName] = response
