import unittest
from typing import Any


class TreeSet:
    """Написано на питоне 3.10 на любой версии меньшей будет выскакивать ошибка из-за типов"""
    def __init__(self, items: list[dict[str, Any]]):
        self.items = items
        self.items_mapping = self.get_parent_mapping()

    def get_parent_mapping(self) -> dict[int, dict[str, list]]:
        """Привожу переданные объекты к удобному для использованию в функциях виду"""
        item_mappings = dict()
        for item in self.items:
            item_mappings[item.get("id")] = dict(
                self_value=item,
                childrens=[
                    row for row in self.items if row.get("parent") == item.get("id")
                ],
                parents=[
                    row for row in self.items if row.get("id") == item.get("parent")
                ],
            )
            for row in item_mappings.get(item["id"]).get("parents"):
                parent_id = row.get("parent")
                if parent_id != "root":
                    item_mappings.get(item["id"])["parents"].append(
                        item_mappings[parent_id].get("self_value")
                    )
        return item_mappings

    def get_all(self) -> list[dict[str, Any]]:  # не уверен насчет названий в camelCase, буду придерживаться стандарта
        """Возвращаем все итемы"""
        return self.items

    def get_item(self, id: int) -> dict[str, Any]:
        """Возвращаем элемент по id"""
        return self.items_mapping.get(id).get("self_value")

    def get_all_parents(self, id: int) -> list[dict[str, Any]]:
        """Возвращаем всех родителей и родителей родителей"""
        return self.items_mapping.get(id).get("parents")

    def get_children(self, id: int) -> list[dict[str, Any]]:
        """Возвращаем все дочерние элементы"""
        return self.items_mapping.get(id).get("childrens")


class TestTree(unittest.TestCase):
    """Небольшой тест для класса с данными"""
    def setUp(self):
        self.items = [
            {"id": 1, "parent": "root"},
            {"id": 2, "parent": 1, "type": "test"},
            {"id": 3, "parent": 1, "type": "test"},
            {"id": 4, "parent": 2, "type": "test"},
            {"id": 5, "parent": 2, "type": "test"},
            {"id": 6, "parent": 2, "type": "test"},
            {"id": 7, "parent": 4, "type": None},
            {"id": 8, "parent": 4, "type": None},
        ]
        self.tree = TreeSet(self.items)

    def test_get_all(self):
        self.assertEqual(self.tree.get_all(), self.items)
        self.assertCountEqual(self.tree.get_all(), self.items)

    def test_get_item(self):
        self.assertEqual(self.tree.get_item(1), self.items[0])
        self.assertEqual(self.tree.get_item(8), self.items[7])

    def test_all_parents(self):
        self.assertEqual(len(self.tree.get_all_parents(8)), 3)
        self.assertEqual(self.tree.get_all_parents(1), [])

    def test_get_children(self):
        self.assertEqual(len(self.tree.get_children(2)), 3)


if __name__ == "__main__":
    unittest.main()