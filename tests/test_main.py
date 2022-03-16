import yaml
from setuptools import setup, find_packages
setup(
    name = 'app',
    packages = find_packages(),
)
from app import main

def test_get_item():
    test_data = yaml.load(open('tests/data/test.yaml'), Loader=yaml.FullLoader)
    print(test_data)
    assert main.get_item(test_data,"root.child1.list[0]") == "element1"
    # assert main.get_item(test_data, "root.child1.list[1]") == "element2"
    # assert main.get_item(test_data, "root.child1.listOfdicts[0].key1") == "element1"
    # assert main.get_item(test_data, "root.child1.list") == ["element1", "element2"]
    # assert main.get_item(test_data, "root.child2") == {"child2t": "text"}
    # assert main.get_item(test_data, "root.child2.child2t") == "text"


if __name__ == "__main__":
    test_get_item()
    print("Everything passed")
