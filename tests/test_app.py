import os
import tempfile
import unittest
from app import create_app

class VelcorisAppTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.close()
        os.environ['DATABASE_PATH'] = self.tmp.name
        os.environ['SECRET_KEY'] = 'test-secret-key'
        os.environ['ADMIN_USERNAME'] = 'testadmin'
        os.environ['ADMIN_PASSWORD'] = 'test-password'
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def tearDown(self):
        try: os.unlink(self.tmp.name)
        except FileNotFoundError: pass
        os.environ.pop('DATABASE_PATH', None)
        os.environ.pop('SECRET_KEY', None)
        os.environ.pop('ADMIN_USERNAME', None)
        os.environ.pop('ADMIN_PASSWORD', None)

    def test_home_and_health(self):
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertEqual(self.client.get('/health').json['status'], 'ok')

    def test_enquiry_validation_and_storage(self):
        payload = {'name':'Test Candidate','email':'candidate@example.com','organisation':'Example Org','enquiry_type':'General enquiry','subject':'Prototype test','message':'This is a synthetic test enquiry.'}
        response = self.client.post('/api/enquiries', data=payload)
        self.assertEqual(response.status_code, 201)
        invalid = self.client.post('/api/enquiries', data={'name':'x','email':'bad','enquiry_type':'Other','subject':'x','message':'short'})
        self.assertEqual(invalid.status_code, 400)

    def test_admin_requires_login_and_can_view(self):
        self.assertEqual(self.client.get('/admin').status_code, 302)
        self.client.post('/admin/login', data={'username':'testadmin','password':'test-password'})
        self.assertEqual(self.client.get('/admin').status_code, 200)

    def test_database_enquiry_retrieval(self):
        payload = {'name':'Database Query Test','email':'querytest@example.com','organisation':'Velcoris Test','enquiry_type':'Technical consultation','subject':'Testing DB Store','message':'Verifying DB storage and retrieval via python-dotenv.'}
        self.client.post('/api/enquiries', data=payload)
        self.client.post('/admin/login', data={'username':'testadmin','password':'test-password'})
        res = self.client.get('/admin')
        self.assertIn(b'Database Query Test', res.data)
        self.assertIn(b'querytest@example.com', res.data)
        self.assertIn(b'Testing DB Store', res.data)

if __name__ == '__main__': unittest.main()
