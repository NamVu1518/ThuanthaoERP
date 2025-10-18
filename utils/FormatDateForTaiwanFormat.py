import re

def format_date(s):
    if not s:
        return ''
    s = s.replace(' ', '')
    arr = s.split('-')
    if len(arr) <= 0 or len(arr) > 2:
        return ''
    elif len(arr) == 1:
        return format_revert(arr[0])
    else:
        return '-'.join([format_revert(x) for x in arr])


def format_revert(s):
    s = s.replace(' ', '')
    arr = s.split('/')
    if len(arr) <= 1:
        if s.lower() == 'nay':
            return 'nay'
        else:
            return s
    else:
        return '/'.join(reversed(arr))

