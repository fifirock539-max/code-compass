import unittest
from catalog import visible_items

class CatalogTests(unittest.TestCase):
    def test_default_hides_archived(self):
        items = [{"id": "a", "archived": False}, {"id": "b", "archived": True}]
        self.assertEqual(visible_items(items), [items[0]])

    def test_explicit_view_keeps_archived(self):
        items = [{"id": "b", "archived": True}]
        self.assertEqual(visible_items(items, True), items)

if __name__ == "__main__":
    unittest.main()
