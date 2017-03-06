def create_elements(element_model, key_list, attr_list, verbose=True, allow_replication=False):
    """
    Assume if key_list is list, then every element has multiple attributes, i.e. attr_list is a multidimensional list
    **Withstand replication check on multi attr element
    **Add MTM relationship only when element is created
    """
    obj_store = []

    for attr in attr_list:
        _cur = {}
        mtm_store = []
        if type(key_list) == list:
            count = 0
            for key in key_list:
                if type(attr[count]) == list and len(attr[count])>0 and type(attr[count][0]) not in [bool, int, str, float, long,]:
                    # Inferred Relationship ManyToMany
                    mtm_store.append((key, attr[count]))
                else:
                    _cur[key] = attr[count]
                count += 1
        else:
            _cur[key_list] = attr
        if verbose:
            print "Trying to create element with dict : {}".format(_cur)
        if allow_replication:
            _x = element_model.objects.create(**_cur)
            created = True
        else:

            _x = element_model.objects.get_or_create(**_cur)
            created = _x[1]
            _x = _x[0]
        obj_store.append(_x)
        if verbose:
            print "Element {} : {} - {}".format("CREATED" if created else "FETCHED", _x.pk, _cur)
        if created:
            for mrel in mtm_store:
                getattr(_x, mrel[0]).add(*mrel[1])
    return obj_store
