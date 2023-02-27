#--- convert set to list
def set_to_list(obj):
    if isinstance(obj, set):
        return sorted(list(obj))
    raise TypeError