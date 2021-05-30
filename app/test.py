from main import app
import unittest


class AppTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def test_add(self):
        response = self.app.post('/pools', json={
            "poolId": 123546,
            "poolValues": [1, 7, 2, 6]
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'inserted')

        response = self.app.post('/pools', json={
            "poolId": 123546,
            "poolValues": 4
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

        response = self.app.post('/pools', json={
            "poolId": 123546,
            "poolValues": "4.0"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

        response = self.app.post('/pools', json={
            "poolId": "123546",
            "poolValues": 4
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

        response = self.app.post('/pools', json={
            "poolId": 123546.0,
            "poolValues": [1, 7, 2, 6]
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'appended')

        response = self.app.post('/pools', json={
            "poolId": 123546.033333,
            "poolValues": [1, 7, 2, 6]
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    def test_get(self):
        self.app.post('/pools', json={
            "poolId": 123546,
            "poolValues": [1, 7, 2, 6]
        }, follow_redirects=True)

        response = self.app.post('/get_quantile', json={
            "poolId": 123546,
            "percentile": 10.0
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['quantile'], 1)
        self.assertEqual(response.json['total_number_elements'], 4)

        self.app.post('/pools', json={
            "poolId": 123546,
            "poolValues": [1, 3, 20, 6]
        }, follow_redirects=True)

        response = self.app.post('/get_quantile', json={
            "poolId": 123546,
            "percentile": 50
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['quantile'], 3)
        self.assertEqual(response.json['total_number_elements'], 8)

        self.app.post('/pools', json={
            "poolId": 9999,
            "poolValues": [1, 3, 20, 6]
        }, follow_redirects=True)
        response = self.app.post('/get_quantile', json={
            "poolId": 123546,
            "percentile": 50
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['quantile'], 3)
        self.assertEqual(response.json['total_number_elements'], 8)

        response = self.app.post('/get_quantile', json={
            "poolId": "123546",
            "percentile": 50
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

        response = self.app.post('/get_quantile', json={
            "poolId": 123546,
            "percentile": "50"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    # executed after each test
    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
