import re

from scrapy.selector import Selector


def _sanitize(input_val, **kwargs):
    """ Shorthand for sanitizing results, removing unicode whitespace and normalizing end result"""
    pattern_re = kwargs.get('pattern_re', '\s+')
    repl_re = kwargs.get('repl_re', ' ')
    flags = kwargs.get('flags', 0)
    post_process = kwargs.get('post_process', lambda x: x)

    if isinstance(input_val, Selector):
        # caller obviously wants clean extracted version
        to_clean = input_val.get()
    else:
        to_clean = input_val

    cleaned = re.sub(pattern_re, repl_re, to_clean.replace('\xa0', ' '), flags=flags).strip()
    return post_process(cleaned)


def clean(lst_or_str, **kwargs):
    """
    Shorthand for sanitizing results in an iterable, dropping ones which would end empty
    :param pattern_re: regex to remove unwanted special characters.
    :param repl_re: regex to replace the pattern_re (unwanted special characters).
    :param post_process: a function that will be called for every sanitized result
    :return: sanitized result.
    """

    if not isinstance(lst_or_str, str) and getattr(lst_or_str, '__iter__', False):  # if iterable and not a string like
        return [x for x in (_sanitize(y, **kwargs) for y in lst_or_str if y is not None) if x]
    return _sanitize(lst_or_str, **kwargs)


def next_request_or_item(item, drop_meta=True):
    if 'meta' not in item:
        return item

    if item['meta']['requests_queue']:
        request = item['meta']['requests_queue'].pop()
        request.meta.setdefault('item', item)
        return request

    item['meta'].pop('requests_queue')
    if drop_meta or not item['meta']:
        item.pop('meta')
    return item
