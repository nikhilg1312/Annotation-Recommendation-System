from SPARQLWrapper import SPARQLWrapper, JSON
import re
import uuid
import base64

as_fair = "http://as-fair-01.ad.maastro.nl:7200/repositories/area51_nickl"
cancer_data = "http://sparql.cancerdata.org/namespace/historical_recommendations/sparql"

label_ip = '"Gender"'
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

print(rq_onto)
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


def uuid_url64():
    """Returns a unique, 16 byte, URL safe ID by combining UUID and Base64
    """
    rv = base64.b64encode(uuid.uuid4().bytes).decode('utf-8')
    return re.sub(r'[\=\+\/]', lambda m: {'+': '-', '/': '_', '=': ''}[m.group(0)], rv)


def runQuery(query, service):
    sparql = SPARQLWrapper(service)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


print(runQuery(get_count_history,cancer_data))