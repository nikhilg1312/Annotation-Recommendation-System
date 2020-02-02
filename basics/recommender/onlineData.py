from SPARQLWrapper import SPARQLWrapper, JSON

wds = "http://as-fair-01.ad.maastro.nl:7200/repositories/area51_nik"

rq_onto = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
select ?iri  ?label ?engLabel where { 
    GRAPH <http://my.graph.sage> 
    {	?iri ?p owl:Class .
        ?iri <http://um-cds/ontologies/databaseontology/column> ?label .
        optional
        {
            ?iri rdfs:label ?engLabel
            filter langMatches( lang(?engLabel), "EN" )
        }
	} 
} 
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


def runQuery():
    sparql = SPARQLWrapper(wds)
    sparql.setQuery(rq_db_column)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


print(runQuery())
