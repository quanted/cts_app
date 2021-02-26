def booleanize(value):
    """
    Django checkbox comes back as 'on' or 'off',
    or True/False depending on version, so this
    makes sure they're True/False.
    """
    if value == 'on' or value == 'true':
        return True
    if value == 'off' or value == 'false' or value == '':
        return False
    if isinstance(value, bool):
        return value