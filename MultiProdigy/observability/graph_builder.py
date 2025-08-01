import json

def trace_to_graph(trace):
    """
    Converts a LangGraph trace into D3.js compatible graph format.
    """
    nodes, links = [], []
    seen = set()

    for step in trace:
        node_id = step["id"]
        if node_id not in seen:
            nodes.append({"id": node_id, "label": step.get("name", ""), "data": step})
            seen.add(node_id)
        for target in step.get("outputs", []):
            links.append({"source": node_id, "target": target["id"], "label": target.get("label", "")})

    return {"nodes": nodes, "links": links}


def save_graph(trace, path="graph_data.json"):
    graph = trace_to_graph(trace)
    with open(path, "w") as f:
        json.dump(graph, f)
