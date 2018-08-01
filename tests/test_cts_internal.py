import requests
import unittest
import numpy.testing as npt
import linkcheck_helper

test = {}

servers = ["https://qedinternal.epa.gov/cts/", "http://127.0.0.1:8000/cts/"]
# servers = ["http://127.0.0.1:8000/cts/"]

pages = {
    'GET': ["", "rest/", "chemspec", "pchemprop", "gentrans", "chemspec/input", "pchemprop/input",
            "gentrans/input", "chemspec/batch", "pchemprop/batch", "gentrans/batch"],
    'POST': []
}

# TODO: replace api_endpoints array with endpoints from cts
api_endpoints = []

# following are lists of url's to be processed with tests below
# check_pages = [s + p for s in servers for p in pages]
check_pages = []
for key,val in pages.items():
    check_pages += [s + p for s in servers for p in pages[key]]

print("check pages: {}".format(check_pages))


class TestCTSPages(unittest.TestCase):
    """
    this testing routine accepts a list of pages and performs a series of unit tests that ensure
    that the web pages are up and operational on the server.
    """

    def setup(self):
        pass

    def teardown(self):
        pass

    @staticmethod
    def test_cts_200():
        test_name = "Check page access "
        try:
            assert_error = False
            response = [requests.get(p).status_code for p in check_pages]
            try:
                npt.assert_array_equal(response, 200, '200 error', True)
            except AssertionError:
                assert_error = True
            except Exception as e:
                # handle any other exception
                print("Error '{0}' occured. Arguments {1}.".format(e.message, e.args))
        except Exception as e:
            # handle any other exception
            print("Error '{0}' occured. Arguments {1}.".format(e.message, e.args))
        finally:
            linkcheck_helper.write_report(test_name, assert_error, check_pages, response)
        return

    @staticmethod
    def test_cts_api_endpoints_200():
        test_name = "Check page access "
        try:
            assert_error = False
            response = [requests.get(p).status_code for p in api_endpoints]
            try:
                npt.assert_array_equal(response, 200, '200 error', True)
            except AssertionError:
                assert_error = True
            except Exception as e:
                # handle any other exception
                print("Error '{0}' occured. Arguments {1}.".format(e.message, e.args))
        except Exception as e:
            # handle any other exception
            print("Error '{0}' occured. Arguments {1}.".format(e.message, e.args))
        finally:
            linkcheck_helper.write_report(test_name, assert_error, api_endpoints, response)
        return

# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()