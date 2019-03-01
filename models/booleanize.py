def booleanize(self, value):
    """
    Django checkbox comes back as 'on' or 'off',
    or True/False depending on version, so this
    makes sure they're True/False.
    """
    if value == 'on' or value == 'true':
        return True
    if value == 'off' or value == 'false':
        return False
    if isinstance(value, bool):
        return value