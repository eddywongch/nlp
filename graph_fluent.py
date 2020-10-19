
from cassandra.cluster import Cluster, EXEC_PROFILE_GRAPH_DEFAULT
from cassandra.datastax.graph import GraphProtocol
from cassandra.datastax.graph.fluent import DseGraph

# Create an execution profile, using GraphSON3 for Core graphs
ep_graphson3 = DseGraph.create_execution_profile(
    'gquotes',
    graph_protocol=GraphProtocol.GRAPHSON_3_0)
cluster = Cluster(execution_profiles={EXEC_PROFILE_GRAPH_DEFAULT: ep_graphson3}, contact_points=['10.101.33.239'])
session = cluster.connect()

# Execute a fluent graph query
g = DseGraph.traversal_source(session=session)

g = DseGraph.traversal_source(session)  # Build the GraphTraversalSource
#print ( g.V().toList() )  # Traverse the Graph


#g.addV('genre').property('genreId', 1).property('name', 'Action').next()

# implicit execution caused by iterating over results
#for v in g.V().has('genre', 'name', 'Drama').in_('belongsTo').valueMap():
#   print(v)
print ( g.V().toList() )