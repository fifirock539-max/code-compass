def visible_items(items, include_archived=False):
    """Return items for a catalog list."""
    if include_archived:
        return list(items)
    return [item for item in items if not item["archived"]]
