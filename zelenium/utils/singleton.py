def _singleton(new_cls):
    instance = new_cls()

    def new(cls):
        if isinstance(instance, cls):
            return instance
        else:
            raise TypeError(
                "I can only return instance of {}, caller wanted {}".format(
                    new_cls, cls
                )
            )

    new_cls.__new__ = new
    new_cls.__init__ = lambda self: None
    return new_cls


def singleton(cls):
    new_cls = type("singleton({})".format(cls.__name__), (cls,), {})
    return _singleton(new_cls)
