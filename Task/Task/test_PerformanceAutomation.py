import time
import unittest
from APIAutomation import get_info


def execution_time(func):
    def run():
        try:
            start_time = time.time_ns()
            res = func()
            return f"Status Code: {res}", "Response Time: {}ms".format(str(float(time.time_ns() - start_time)*1000000)[0:5])
        except Exception as error:
            print(error)
            return None
    return run


@execution_time
def test_api():
    url = "https://goerli.infura.io/v3/01e65d54328e4c7185f9069b66dba1d5"
    wallet_id = '0x256144a60f34288F7b03D345F8Cb256C502e0f2C'
    p = get_info(url, wallet_id)
    return p[1]


class TestApi(unittest.TestCase):
    def runTest(self):
        url = "https://goerli.infura.io/v3/01e65d54328e4c7185f9069b66dba1d5"
        wallet_id = '0x256144a60f34288F7b03D345F8Cb256C502e0f2C'
        p = get_info(url, wallet_id)
        self.assertIsNotNone(p)


if __name__ == '__main__':
    TestApi().runTest()
    #res = test_api()
    #print(*res)


