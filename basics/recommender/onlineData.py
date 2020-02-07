from SPARQLWrapper import SPARQLWrapper, JSON
import re
import uuid
import base64
import json
import pandas as pd


def uuid_url64():
    """Returns a unique, 16 byte, URL safe ID by combining UUID and Base64
    """
    rv = base64.b64encode(uuid.uuid4().bytes).decode('utf-8')
    return re.sub(r'[\=\+\/]', lambda m: {'+': '-', '/': '_', '=': ''}[m.group(0)], rv)


qwe = "http://" + uuid_url64()

as_fair = "http://as-fair-01.ad.maastro.nl:7200/repositories/area51_nickl"
cancer_data = "http://sparql.cancerdata.org/namespace/historical_recommendations/sparql"

label_ip = '"female"'
rq_onto = f"""
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
select ?iri  ?label ?engLabel where {{ 
    GRAPH <http://my.graph.sage> 
    {{	?iri ?p owl:Class .
        ?iri <http://um-cds/ontologies/databaseontology/column> ?label .
        optional
        {{
            ?iri rdfs:label {label_ip}
            filter langMatches( lang(?engLabel), "EN" )
        }}
	}} 
}} 
"""

rq_db_column = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select ?iri ?label ?def where { 
    GRAPH <http://localhost/ontology/roo> { 
        ?iri rdfs:label ?label .        
                optional
                {
                    ?iri <http://www.w3.org/2004/02/skos/core#definition> ?def.
                    ?iri ?p owl:Class .
                }
    }
} 
"""

get_count_history = f"""
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>

select ?o1 (count(?o1) as ?count)
where
{{
  ?s rdf:type ?o1;
     rdfs:label {label_ip}
}}
group by ?o1
"""


def insert_history_cancerdataorg(label, iri):
    uid = "http://" + uuid_url64()

    insert_sparql = f""" 
    insert data
    {{
    	<{uid}>   <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>   <{iri}>.
    	<{uid}>   <http://www.w3.org/2000/01/rdf-schema#label>   "{label}".	
    }}
    """

    print(insert_sparql)
    runQuery(insert_sparql, cancer_data)
    print("History Upload successful")
    return 1


def get_label_history(label):
    uid = "http://" + uuid_url64()

    get_count_sparql = f""" 
        prefix roo: <http://www.cancerdata.org/roo/>
        prefix ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix icd: <http://purl.bioontology.org/ontology/ICD10/>
        prefix uo: <http://purl.obolibrary.org/obo/UO_>
        prefix ro: <http://www.radiomics.org/RO/>
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        select ?iri (count(?iri) as ?count)
        where
        {{
          ?s rdf:type ?iri;
             rdfs:label ?label
          FILTER regex(?label, "{label}", "i")
        }}
        group by ?iri
        order by desc(?count)
        limit 2
    """

    sparql = SPARQLWrapper(cancer_data)
    sparql.setQuery(get_count_sparql)
    sparql.setReturnFormat(JSON)
    result = sparql.query()

    processed_results = json.load(result.response)
    cols = processed_results['head']['vars']

    out = []
    for row in processed_results['results']['bindings']:
        item = []
        for c in cols:
            item.append(row.get(c, {}).get('value'))
        out.append(item)

    return pd.DataFrame(out, columns=cols)


def runQuery(query, service):
    sparql = SPARQLWrapper(service)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def online_count_history_find(label):
    history = []
    his_df = get_label_history(label)

    if his_df.empty:
        print("in return_historical_finds :: NOT FOUND ")
        return "Not found"
    else:
        for h in his_df.itertuples(index=False):
            history.append({"label": label, 'iri': h.iri, 'match_ratio': h.count})
        return history


print(online_count_history_find("gender"))
