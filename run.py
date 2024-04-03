from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

# Specify the SPARQL endpoint URL
sparql_endpoint = "http://statistics.gov.scot/sparql"

# Initialize SPARQLWrapper with the endpoint
sparql = SPARQLWrapper(sparql_endpoint)

# Set the SPARQL query
sparql.setQuery("""
PREFIX dimension: <http://statistics.gov.scot/def/dimension/>
PREFIX sdmxDimension: <http://purl.org/linked-data/sdmx/2009/dimension#>
PREFIX measure: <http://statistics.gov.scot/def/measure-properties/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?applicationTypeLabel ?refAreaLabel ?refPeriod ?count
WHERE {
  ?record dimension:applicationType ?applicationType .
  ?record sdmxDimension:refArea ?refArea .
  ?record sdmxDimension:refPeriod ?refPeriodURI .
  ?record measure:count ?count .
  
  OPTIONAL { ?applicationType rdfs:label ?applicationTypeLabel . }
  OPTIONAL { ?refArea rdfs:label ?refAreaLabel . }
  OPTIONAL { ?refPeriodURI rdfs:label ?refPeriod . }
}
LIMIT 100
""")

# Set the return format to JSON
sparql.setReturnFormat(JSON)

# Execute the query and convert the result to a Python dictionary
results = sparql.query().convert()

# Convert the SPARQL results to a Pandas DataFrame
data = {
    'Application Type': [result['applicationTypeLabel']['value'] if 'applicationTypeLabel' in result else None for result in results["results"]["bindings"]],
    'Reference Area': [result['refAreaLabel']['value'] if 'refAreaLabel' in result else None for result in results["results"]["bindings"]],
    'Reference Period': [result['refPeriod']['value'] if 'refPeriod' in result else None for result in results["results"]["bindings"]],
    'Count': [float(result['count']['value']) if 'count' in result else None for result in results["results"]["bindings"]]  # Assuming count is a numeric value
}

df = pd.DataFrame(data)

# Display the first few rows of the DataFrame
print(df.head())
