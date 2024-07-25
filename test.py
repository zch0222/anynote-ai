from duckduckgo_search import DDGS
from pprint import pprint


if __name__ == '__main__':
    with DDGS() as ddgs:
        pprint([r for r in ddgs.text("阿里云", region='cn-zh', max_results=10)])
