'''
Created on 24.4.2012

@author: Andrew
'''

import yandex_maps.tests as tests

tests.TEST_API_KEY = 'AJ-8lk8BAAAA-XpFDwQAoJN8eB59A0iz1F1M1tRGnzO-7H0AAAAAAAAAAABMVbn1rJgaBBtgmNsMsBM0CTAf7A=='

if (__name__ == "__main__"):
    from tests import MapUrlTest
    mapurltest = MapUrlTest('test_map_url')
    mapurltest.test_map_url()
