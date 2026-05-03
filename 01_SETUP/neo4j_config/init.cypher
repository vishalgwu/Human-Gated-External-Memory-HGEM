// HGEM Neo4j initialization
// Role: T2 validated memory graph.

CREATE CONSTRAINT validated_node_entry_id IF NOT EXISTS
FOR (n:ValidatedNode)
REQUIRE n.entry_id IS UNIQUE;

CREATE INDEX validated_node_session_step IF NOT EXISTS
FOR (n:ValidatedNode)
ON (n.session_id, n.step_number);

CREATE INDEX validated_node_benchmark IF NOT EXISTS
FOR (n:ValidatedNode)
ON (n.benchmark);

// Required relationship types used by HGEM:
// (:ValidatedNode)-[:DEPENDS_ON]->(:ValidatedNode)
// (:ValidatedNode)-[:LEADS_TO]->(:ValidatedNode)
// (:ValidatedNode)-[:CONTRADICTS]->(:ValidatedNode)
// (:ValidatedNode)-[:CONFIRMS]->(:ValidatedNode)

