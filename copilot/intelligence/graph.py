from __future__ import annotations


def get_intelligence_graph() -> dict:
    nodes = [
        "historical",
        "pricing",
        "market",
        "forecast",
        "capacity",
        "risk",
        "decision",
        "recommendation",
        "explainability",
    ]

    edges = [
        {
            "source": "historical",
            "target": "pricing",
            "relationship": "informs",
        },
        {
            "source": "historical",
            "target": "forecast",
            "relationship": "informs",
        },
        {
            "source": "pricing",
            "target": "market",
            "relationship": "signals",
        },
        {
            "source": "market",
            "target": "risk",
            "relationship": "affects",
        },
        {
            "source": "capacity",
            "target": "risk",
            "relationship": "affects",
        },
        {
            "source": "forecast",
            "target": "decision",
            "relationship": "contributes_to",
        },
        {
            "source": "pricing",
            "target": "decision",
            "relationship": "contributes_to",
        },
        {
            "source": "capacity",
            "target": "decision",
            "relationship": "contributes_to",
        },
        {
            "source": "risk",
            "target": "decision",
            "relationship": "contributes_to",
        },
        {
            "source": "decision",
            "target": "recommendation",
            "relationship": "produces",
        },
        {
            "source": "recommendation",
            "target": "explainability",
            "relationship": "explained_by",
        },
    ]

    return {
        "summary": {
            "status": "intelligence graph available",
            "node_count": len(nodes),
            "edge_count": len(edges),
        },
        "nodes": nodes,
        "edges": edges,
    }
