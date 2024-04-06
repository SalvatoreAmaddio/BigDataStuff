"""
INTRO TO SPARQL:

SPARQL is a query language used to navigate the web.
It can return webpages, datasets, videos and more!
It uses an endpoint against which you can your queries.
It looks like SQL but it is not.

This technology allows you to access to a given end point and retrieve
a dataset from it.

It is the goal of this developer to learn more about this technology 
in the near future.

You can read more about SPARQL here: 
https://www.ontotext.com/knowledgehub/fundamentals/what-is-sparql/
https://www.w3.org/TR/sparql11-query/

Tutorials:
https://www.youtube.com/watch?v=r7N7s1yejFQ&list=PLea0WJq13cnA6k4B6Tr1ljj2nleUl9dZt&index=1

API DOCUMENTATION:
https://statistics.gov.scot/resource?uri=http%3A%2F%2Fstatistics.gov.scot%2Fdata%2Fscottish-health-survey-scotland-level-data
"""

from SPARQLWrapper import SPARQLWrapper, JSON

def AsHumanReadable(column, label:str):
    """
    This is a function that will be used at the end of this file.
    This function is used to adjust the value of a dictionary and 
    return human readble values 
    """
    return [column[label]['value'] if label in column else None for column in column["results"]["bindings"]],


end_point = "http://statistics.gov.scot/sparql"
# Initialize the SPARQL wrapper with the endpoint URL
sparql = SPARQLWrapper(end_point)

"""
This query took hours to build. Even though I can explain line by line
what it does, I am still not confident enough in altering the structure as I cannot
predict what results can yield. 

At the moment we can follow the filosopy: 
If it is not broken, do not touch it.
"""
# Set your SPARQL query
sparql.setQuery("""
PREFIX qb: <http://purl.org/linked-data/cube#>
PREFIX sdmxDimension: <http://purl.org/linked-data/sdmx/2009/dimension#>
PREFIX scotDimension: <http://statistics.gov.scot/def/dimension/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT  ?refAreaLabel ?refPeriodLabel ?indicatorLabel ?sexLabel ?measureTypeLabel ?value
WHERE {
    ?observation a qb:Observation ;
                 sdmxDimension:refArea ?refArea ;
                 sdmxDimension:refPeriod ?refPeriod ;
                 scotDimension:scottishHealthSurveyIndicator ?indicator ;
                 scotDimension:sex ?sex ;
                 qb:measureType ?measureType ;
                 ?measureType ?value .

    OPTIONAL { ?refArea rdfs:label ?refAreaLabel . }
    OPTIONAL { ?refPeriod rdfs:label ?refPeriodLabel . }
    OPTIONAL { ?indicator rdfs:label ?indicatorLabel . }
    OPTIONAL { ?sex rdfs:label ?sexLabel . }
    OPTIONAL { ?measureType rdfs:label ?measureTypeLabel . }
}
LIMIT 11881
""")

#Return the result as JSON
sparql.setReturnFormat(JSON)

#Run the query, the JSON result will be converted into a Python dictionary
results = sparql.query().convert()

#Redefine the dictionary to display human readable values.
data = {
    'Reference Area': [result['refAreaLabel']['value'] if 'refAreaLabel' in result else None for result in results["results"]["bindings"]],
    'Reference Period': [result['refPeriodLabel']['value'] if 'refPeriodLabel' in result else None for result in results["results"]["bindings"]],
    'Indicator': [result['indicatorLabel']['value'] if 'indicatorLabel' in result else None for result in results["results"]["bindings"]],
    'Sex': [result['sexLabel']['value'] if 'sexLabel' in result else None for result in results["results"]["bindings"]],
    'Measure Type': [result['measureTypeLabel']['value'] if 'measureTypeLabel' in result else None for result in results["results"]["bindings"]],
    'Value': [result['value']['value'] if 'value' in result else None for result in results["results"]["bindings"]]
}



