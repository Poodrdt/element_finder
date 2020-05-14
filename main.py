"""
usage: main.py [-h] train test

positional arguments:
  train        analyzed file path
  test         searched file path
"""
from bs4 import BeautifulSoup
import argparse
from xpath import get_css_path

TARGET = "make-everything-ok-button"

parser = argparse.ArgumentParser()
parser.add_argument("train")
parser.add_argument("test")

args = parser.parse_args()


def get_sample_element():
    with open(args.train, 'r') as f:
        train_page = f.read()
    train_soup = BeautifulSoup(train_page, "lxml")
    return train_soup.find(id=TARGET)


def find_similar_elements(sample_elem):
    similar_elements = {}
    with open(args.test, 'r') as f:
        test_page = f.read()
    test_soup = BeautifulSoup(test_page, "lxml")
    for k, v in sample_elem.attrs.items():
        for i in test_soup.find_all("", {k: v}):
            similar_elements.update({get_css_path(i): i})
    return similar_elements


def find_most_similar(sample_element, similar_elements):
    max_weight, elem_xpath = 0, None
    for xpath, similar_element in similar_elements.items():
        elem_weight = get_element_weight(sample_element, similar_element)
        if elem_weight > max_weight:
            max_weight, elem_xpath = elem_weight, xpath
    print(f"max matched {max_weight} attributes")
    return elem_xpath


def get_element_weight(sample_element, similar_element):
    weight = 0
    for k, v in sample_element.attrs.items():
        if similar_element.attrs.get(k) == v:
            print(f"Attribute '{k}' matched with value '{v}'")
            weight += 1
    print(f"matched {weight} attributes")
    return weight


def main():
    target = get_sample_element()
    similar = find_similar_elements(target)
    most_similar = find_most_similar(target, similar)
    print(get_css_path(target))
    print(most_similar)


main()
