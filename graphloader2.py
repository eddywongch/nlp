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

#g = DseGraph.traversal_source(session)  # Build the GraphTraversalSource

#traversal = g.traversal()

 # locate person vertex
traversal1 = g.V() \
        .has('person', 'name', 'Chet Kappor').as_('^chet')

traversal2 = g.V() \
        .has('quote', 'quote_id', 'daa02698-df4f-4436-8855-941774f4c3e0').as_('^quote')


traversal3 = g.V() \
        .has('keyword', 'key', 'cassandra').as_('^cass')


# add edge from user to video vertex
traversal = traversal3.addE('foundin') \
        .to(g.V().has('quote', 'quote_id', 'daa02698-df4f-4436-8855-941774f4c3e0'))

#  .from_('^cass').to('^quote').iterate()


# Execute the traversal
traversal.iterate()