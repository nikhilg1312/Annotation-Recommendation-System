import json

columns_json = open("/home/nikhil/Documents/Projects/flask_tutorials/basics/recommender/static/DB_labels.srj", "r")
ontology_json = open("/home/nikhil/Documents/Projects/flask_tutorials/basics/recommender/static/onto.srj", "r")

columns_df = json.load(columns_json)
ontology_df = json.load(ontology_json)


def extract_element_from_json(obj, path):
    '''
    Extracts an element from a nested dictionary or
    a list of nested dictionaries along a specified path.
    If the input is a dictionary, a list is returned.
    If the input is a list of dictionary, a list of lists is returned.
    obj - list or dict - input dictionary or list of dictionaries
    path - list - list of strings that form the path to the desired element
    '''

    def extract(obj, path, ind, arr):
        '''
            Extracts an element from a nested dictionary
            along a specified path and returns a list.
            obj - dict - input dictionary
            path - list - list of strings that form the JSON path
            ind - int - starting index
            arr - list - output list
        '''
        key = path[ind]
        if ind + 1 < len(path):
            if isinstance(obj, dict):
                if key in obj.keys():
                    extract(obj.get(key), path, ind + 1, arr)
                else:
                    arr.append(None)
            elif isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        extract(item, path, ind, arr)
            else:
                arr.append(None)
        if ind + 1 == len(path):
            if isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        arr.append(item.get(key, None))
            elif isinstance(obj, dict):
                arr.append(obj.get(key, None))
            else:
                arr.append(None)
        return arr

    if isinstance(obj, dict):
        return extract(obj, path, 0, [])
    elif isinstance(obj, list):
        outer_arr = []
        for item in obj:
            outer_arr.append(extract(item, path, 0, []))
        return outer_arr


# print(json.dumps(columns_df["results"], indent = 4, sort_keys=True))
def get_column_names():
    # todo should we have a logic which removes column labels?
    ex_dump = []

    label_df = extract_element_from_json(columns_df["results"], ["bindings", "label", "value"])
    iri_df = extract_element_from_json(columns_df["results"], ["bindings", "iri", "value"])
    engLabel_df = extract_element_from_json(columns_df["results"], ["bindings", "engLabel", "value"])

    for l, i, d in zip(label_df, iri_df, engLabel_df):
        d = d.partition(".")[2]
        onto_temp = {'label': l, 'iri': i, 'engLabel': d}
        ex_dump.append(onto_temp)

    return ex_dump


def get_ontology_labels():
    # todo get ontology label
    main_case = []
    label_df = extract_element_from_json(ontology_df["results"], ["bindings", "label", "value"])
    iri_df = extract_element_from_json(ontology_df["results"], ["bindings", "iri", "value"])
    def_df = extract_element_from_json(ontology_df["results"], ["bindings", "def", "value"])

    for l, i, d in zip(label_df, iri_df, def_df):
        onto_temp = {'label': l, 'iri': i, 'definition': d}
        main_case.append(onto_temp)

    return json.dumps(main_case)


print(get_column_names())
