import sys
import requests
import unittest
import numpy.testing as npt
# import linkcheck_helper
import cts_app.tests.linkcheck_helper as linkcheck_helper
from cts_app.tests.test_objects import get_post_object
from django.test import Client, TestCase

test = {}

# servers = ["https://qedinternal.epa.gov/cts/", "http://127.0.0.1:8000/cts/"]
servers = ["http://127.0.0.1:8000/cts/"]

pages = ["", "rest/", "chemspec", "pchemprop", "gentrans",
        "chemspec/input", "pchemprop/input", "gentrans/input",
        "chemspec/batch", "pchemprop/batch", "gentrans/batch"]

# output_pages = ["chemspec/output", "pchemprop/output", "gentrans/output"]  # require POST
workflow_endpoints = ["/cts/chemspec/output"]  # require POST  (returned a CSRF 403..)

# TODO: replace api_endpoints array with endpoints from cts
api_endpoints = []

# following are lists of url's to be processed with tests below
check_pages = [s + p for s in servers for p in pages]

# workflow_test_urls = [s + p for s in servers for p in output_pages]

print("checking pages: {}".format(check_pages))
# print("checking workflow outputs at: {}".format(workflow_test_urls))


# class TestCTSPages(unittest.TestCase):
class TestCTSPages(TestCase):
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
    def test_cts_workflows():

        test_client = Client()

        test_name = "Check workflow outputs "
        try:
            assert_error = False
            # response = [requests.get(p).status_code for p in check_pages]

            response = []
            for p in workflow_endpoints:
                workflow = p.split('/')[0]  # assuming model/output url structure, grabbing "model" part

                post_data = get_post_object(workflow)

                print("workflow: {}".format(workflow))
                print("url: {}".format(p))
                print("post: {}".format(post_data))

                res = test_client.post(p, get_post_object(workflow))


                response.append(res.status_code)
            try:

                print(">>> Response: {}".format(response))

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
            print("response: {}".format(response))
            linkcheck_helper.write_report(test_name, assert_error, workflow_endpoints, response)
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