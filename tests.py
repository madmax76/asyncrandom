#!/usr/bin/env python
import sys

from tornado import testing
from tornado import escape
from tornado import concurrent
from tornado import httpclient

import asyncrandom

if sys.version_info[0] < 3:
    from mock import patch
    from mock import Mock
    from StringIO import StringIO
else:
    from unittest.mock import patch
    from unittest.mock import Mock
    from io import StringIO


def fetch_mock(status_code, body_data):

    def side_effect(request, **kwargs):
        if request is not httpclient.HTTPRequest:
            request = httpclient.HTTPRequest(request)

        body = StringIO(escape.json_encode(body_data))
        response = httpclient.HTTPResponse(request, status_code, None, body)
        future = concurrent.Future()
        future.set_result(response)
        return future

    fetch_mock = Mock(side_effect=side_effect)
    return fetch_mock


FETCH_METHOD = "tornado.httpclient.AsyncHTTPClient.fetch"


class TestWithMock(testing.AsyncTestCase):

    @patch(FETCH_METHOD, fetch_mock(404, None))
    @testing.gen_test
    def test_not_found(self):
        with self.assertRaises(httpclient.HTTPError) as e:
            yield asyncrandom.fetch()
        httpclient.AsyncHTTPClient.fetch.assert_called_with(
            "https://qrng.anu.edu.au/API/jsonI.php?length=1&type=uint8")
        self.assertEqual(e.exception.code, 404)

    @patch(FETCH_METHOD, fetch_mock(500, None))
    @testing.gen_test
    def test_server_error(self):
        with self.assertRaises(httpclient.HTTPError) as e:
            yield asyncrandom.fetch()
        httpclient.AsyncHTTPClient.fetch.assert_called_with(
            "https://qrng.anu.edu.au/API/jsonI.php?length=1&type=uint8")
        self.assertEqual(e.exception.code, 500)

    @patch(FETCH_METHOD, fetch_mock(200, {"success": True, "data": [42]}))
    @testing.gen_test
    def test_success_single_uint8(self):
        value = yield asyncrandom.fetch()
        httpclient.AsyncHTTPClient.fetch.assert_called_with(
            "https://qrng.anu.edu.au/API/jsonI.php?length=1&type=uint8")
        self.assertEqual(value, 42)

    @patch(FETCH_METHOD, fetch_mock(200, {"success": True, "data": [100, 101]}))
    @testing.gen_test
    def test_success_multiple_uint8(self):
        values = yield asyncrandom.fetch(length=2)
        httpclient.AsyncHTTPClient.fetch.assert_called_with(
            "https://qrng.anu.edu.au/API/jsonI.php?length=2&type=uint8")
        self.assertListEqual(values, [100, 101])

    @patch(FETCH_METHOD, fetch_mock(200, {"success": True, "data": [34500]}))
    @testing.gen_test
    def test_success_single_uint16(self):
        value = yield asyncrandom.fetch(
            int_type=asyncrandom.IntegerType.UINT16)
        httpclient.AsyncHTTPClient.fetch.assert_called_with(
            "https://qrng.anu.edu.au/API/jsonI.php?length=1&type=uint16")
        self.assertEqual(value, 34500)

    @patch(FETCH_METHOD, fetch_mock(
        200, {"success": True, "data": [3450, 10001]}))
    @testing.gen_test
    def test_success_multiple_uint16(self):
        values = yield asyncrandom.fetch(
            length=2, int_type=asyncrandom.IntegerType.UINT16)

        httpclient.AsyncHTTPClient.fetch.assert_called_with(
            "https://qrng.anu.edu.au/API/jsonI.php?length=2&type=uint16")
        self.assertListEqual(values, [3450, 10001])

    @patch(FETCH_METHOD, fetch_mock(200, {"success": False}))
    @testing.gen_test
    def test_unsuccessful(self):
        with self.assertRaises(ValueError):
            yield asyncrandom.fetch()

        httpclient.AsyncHTTPClient.fetch.assert_called_with(
            "https://qrng.anu.edu.au/API/jsonI.php?length=1&type=uint8")

    @patch(FETCH_METHOD, fetch_mock(200, {"success": False}))
    @testing.gen_test
    def test_negative_length(self):
        with self.assertRaises(TypeError):
            yield asyncrandom.fetch(length=-1)


@testing.unittest.skipUnless(__name__ == "__main__", "skipping external tests")
class TestRealAPI(testing.AsyncTestCase):
    # Skip tests against the real API unless the file has been called explcitly
    # from the command line.
    # If the tests are run through e.g. nose or setup.py, these tests will not
    # run.

    @testing.gen_test(timeout=10)
    def test_single_uint8(self):
        value = yield asyncrandom.fetch()
        self.assertIsInstance(value, int)
        self.assertLessEqual(value, 255)

    @testing.gen_test(timeout=10)
    def test_multiple_uint8(self):
        values = yield asyncrandom.fetch(length=20)
        self.assertIsInstance(values, list)
        self.assertEqual(len(values), 20)
        for random_num in values:
            self.assertLessEqual(random_num, 255)

    @testing.gen_test(timeout=10)
    def test_single_uint16(self):
        value = yield asyncrandom.fetch(
            int_type=asyncrandom.IntegerType.UINT16)
        self.assertIsInstance(value, int)
        self.assertLessEqual(value, 65535)

    @testing.gen_test(timeout=10)
    def test_multiple_uint16(self):
        values = yield asyncrandom.fetch(
            length=20, int_type=asyncrandom.IntegerType.UINT16)
        self.assertIsInstance(values, list)
        self.assertEqual(len(values), 20)
        for random_num in values:
            self.assertLessEqual(random_num, 65535)

    @testing.gen_test
    def test_incorrect_length_value(self):
        with self.assertRaises(TypeError):
            yield asyncrandom.fetch(length="1")

    @testing.gen_test
    def test_incorrect_type_value(self):
        with self.assertRaises(TypeError):
            yield asyncrandom.fetch(int_type="uint8")


if __name__ == "__main__":
    testing.unittest.main()
