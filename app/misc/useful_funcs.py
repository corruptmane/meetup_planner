from typing import List


def generate_pages(array: List, articles_on_page: int) -> List[List]:
    length = len(array)
    number_of_pages = (length // articles_on_page)
    if length % articles_on_page != 0:
        number_of_pages += 1
    results = [array[page * articles_on_page : (page + 1) * articles_on_page] for page in range(number_of_pages)]
    return results


__all__ = ("generate_pages")
