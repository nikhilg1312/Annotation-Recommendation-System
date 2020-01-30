from SPARQLWrapper import SPARQLWrapper, JSON

wds = "http://as-fair-01.ad.maastro.nl:7200/repositories/area51_nik"

rq_onto = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select ?iri ?label ?def  
where 
{ 
    ?iri rdfs:label ?label .
    optional
    {
        ?iri <http://www.w3.org/2004/02/skos/core#definition> ?def.
        ?iri ?p owl:Class .
    }
} 
"""

rq_db_column = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
select ?s  ?label ?engLabel 
where 
{ 
                                        {	?s ?p owl:Class .
                                            ?s <http://um-cds/ontologies/databaseontology/column> ?label .
                                            FILTER regex(str(?s), "http://localhost/rdf/ontology/Outcome*", "i")
                                            optional
                                            {
                                                ?s rdfs:label ?engLabel
                                                filter langMatches( lang(?engLabel), "EN" )
                                            }
                                        } 
UNION
                                        {
                                                ?s ?p owl:Class .
                                                ?s <http://um-cds/ontologies/databaseontology/column> ?label .
                                                FILTER regex(str(?s), "http://localhost/rdf/ontology/Tumour_Treatment*", "i")
                                                optional
                                                {
                                                    ?s rdfs:label ?engLabel
                                                    filter langMatches( lang(?engLabel), "EN" )
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
