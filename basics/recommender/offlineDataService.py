import json, re
from fuzzywuzzy import process
from pyjarowinkler import distance
import pandas as pd
import spacy

pd.set_option('display.width', 900)
pd.set_option('display.max_columns', 10)


nlp = spacy.load('en_core_sci_lg')


def insert(df, row):
    insert_loc = df.index.max()
    if pd.isna(insert_loc):
        df.loc[0] = row
    else:
        df.loc[insert_loc + 1] = row


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


columns_json = open("/home/nikhil/Documents/Projects/flask_tutorials/basics/recommender/static/DB_labels.srj", "r")
ontology_json = open("/home/nikhil/Documents/Projects/flask_tutorials/basics/recommender/static/onto.srj", "r")

columns_df = json.load(columns_json)
ontology_list = json.load(ontology_json)

all_columns = []
onto_full = []

label_df = extract_element_from_json(ontology_list["results"], ["bindings", "label", "value"])
iri_df = extract_element_from_json(ontology_list["results"], ["bindings", "iri", "value"])
def_df = extract_element_from_json(ontology_list["results"], ["bindings", "def", "value"])

ontology_df = pd.DataFrame(columns=['iri', 'label', 'def'])
for l, i, d in zip(label_df, iri_df, def_df):
    ontology_df = ontology_df.append(
        pd.Series({'label': str.strip(str(l)), 'iri': str.strip(str(i)), 'def': str.strip(str(d))}), ignore_index=True)


# print(json.dumps(columns_df["results"], indent = 4, sort_keys=True))
def get_column_names():
    label_df = extract_element_from_json(columns_df["results"], ["bindings", "label", "value"])
    iri_df = extract_element_from_json(columns_df["results"], ["bindings", "iri", "value"])
    eng_label_df = extract_element_from_json(columns_df["results"], ["bindings", "engLabel", "value"])

    for l, i, d, id in zip(label_df, iri_df, eng_label_df, range(len(label_df))):
        # d = d.partition(".")[2]
        # regex = r"\gy/(.*?)\."
        table = "TableName"
        onto_temp = {'id': id, 'label': l, 'iri': i, 'engLabel': d, 'table': table}
        all_columns.append(onto_temp)

    return all_columns

cvb = get_column_names()
a = 1+2

def get_ontology_labels():
    iri_df = extract_element_from_json(ontology_list["results"], ["bindings", "iri", "value"])
    def_df = extract_element_from_json(ontology_list["results"], ["bindings", "def", "value"])

    for l, i, d in zip(label_df, iri_df, def_df):
        onto_temp = {'label': l, 'iri': i, 'definition': d}
        onto_full.append(onto_temp)

    return json.dumps(onto_full)


def get_selected_column(selected_id, posts):
    selected_column = []
    for p in posts:
        for s in selected_id:
            if int(p["id"]) == int(s):
                selected_column.append({
                    'label': p["label"],
                    'iri': p["iri"],
                    'engLabel': p["engLabel"],
                    'table': p["table"],
                    'id': p["id"],
                    'predicted': get_predicted_labels(p["engLabel"]),
                    'history': return_historical_finds(p["engLabel"])
                })
    return selected_column


def get_selected_column_post(selected_id, posts):
    selected_column = []
    for p in posts:
            if int(p["id"]) == selected_id:
                selected_column.append({
                    'label': p["label"],
                    'iri': p["iri"],
                    'engLabel': p["engLabel"],
                    'table': p["table"],
                    'id': p["id"],
                    'predicted': get_predicted_labels(p["engLabel"]),
                    'history': return_historical_finds(p["engLabel"])
                })
    return selected_column


def get_levenstein_pred(ip_label):
    predicted_label = process.extractOne(ip_label, label_df)
    return predicted_label[0]


def get_jaroWrinkler_pred(ip_label):
    distance_df = pd.DataFrame(columns=['ip', 'm_tk', '%match'])
    for t in label_df:
        asd = distance.get_jaro_distance(ip_label, t, winkler=True, scaling=0.1)
        insert(distance_df, [ip_label, t, asd * 100])
    val = distance_df.loc[distance_df['%match'].idxmax()]
    return val[1]


def get_similar_ontology_term_nlp(term):
    op_df = pd.DataFrame(columns=["term", "match%"])
    n_term = nlp(str.lower(term))

    for onto_term in label_df:
        n_onto_term = nlp(str.lower(onto_term))
        op_df = op_df.append(pd.Series([onto_term, n_term.similarity(n_onto_term)], index=op_df.columns),
                             ignore_index=True)
    max2_df = op_df.nlargest(2, "match%")
    p1 = max2_df.iloc[0, 0]
    p2 = max2_df.iloc[1, 0]
    return p1, p2


def search_iri_for_label(term, src_df):
    iri = src_df.query("{0} == '{1}' ".format("label", str.strip(term))).iloc[0, 0]
    return iri


def count_unique_index(df, by):
    return df.groupby(by).size().reset_index().rename(columns={0: 'count'})


def return_historical_finds(search_str):
    history = []
    ip_df = pd.read_csv("/home/nikhil/Documents/Projects/base_standard/gold_std/ip.csv")
    temp = pd.DataFrame()
    temp['DB_lower'] = ip_df['DB'].str.lower()
    ip_df = ip_df.join(temp)

    ip_df = count_unique_index(ip_df, ['DB', 'Ontology','DB_lower'])
    ip_df = ip_df.loc[ip_df.DB_lower == str.lower(search_str)]
    total_count = ip_df["count"].sum()

    if total_count == 0:
        print("in return_historical_finds :: NOT FOUND ")
        return "Not found"
    else:
        match_ratio = (ip_df['count'] / total_count) * 100
        ip_df = ip_df.assign(match_ratio=match_ratio.values)
        ip_df = ip_df.nlargest(1, 'match_ratio')

        for i in ip_df.itertuples(index=False):
            history.append({"label": i.DB, 'iri': i.Ontology, 'match_ratio': i.match_ratio})
    return history


def get_predicted_labels(ip_label):
    predicted_labels_with_iri = []
    lv = get_levenstein_pred(ip_label)
    lv_iri = search_iri_for_label(lv, ontology_df)
    jw = get_jaroWrinkler_pred(ip_label)
    jw_iri = search_iri_for_label(jw, ontology_df)
    #p1, p2 = get_similar_ontology_term_nlp(ip_label)
    #p1_iri = search_iri_for_label(p1, ontology_df)
    #p2_iri = search_iri_for_label(p2, ontology_df)

    predicted_labels_with_iri.append({'label': lv, 'iri': lv_iri})
    predicted_labels_with_iri.append({'label': jw, 'iri': jw_iri})
    #predicted_labels_with_iri.append({'label': p1, 'iri': p1_iri})
    #predicted_labels_with_iri.append({'label': p2, 'iri': p2_iri})

    return predicted_labels_with_iri
