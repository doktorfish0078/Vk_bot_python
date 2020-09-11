def find_common(orig, list_to_search_in):
    for elem in list_to_search_in:
        if elem == orig:
            return True
    return False