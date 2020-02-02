import pandas as pd
import json
from SPARQLWrapper import SPARQLWrapper, JSON


def get_sparql_dataframe(service, query):
    """
    Helper function to convert SPARQL results into a Pandas data frame.
    """
    sparql = SPARQLWrapper(service)
    sparql.setQuery(query)
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


wds = "http://as-fair-01.ad.maastro.nl:7200/repositories/nik_area51"

rq = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select ?s ?label  where { 
	?s rdfs:label ?label .
    FILTER regex(?label, "has_*", "i")

} 

"""

df = get_sparql_dataframe(wds, rq)

print(df)
