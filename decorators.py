def lower_case(func):
    def closure(*args, **kwargs):
        for k in kwargs:
            if isinstance(kwargs[k], str)\
                    or isinstance(kwargs[k], unicode):
                kwargs[k] = kwargs[k].lower()

        lower_args = []

        for arg in args:
            if isinstance(arg, str)\
                    or isinstance(arg, unicode):
                lower_args.append(arg.lower())

        return func(*lower_args, **kwargs)

    return closure
