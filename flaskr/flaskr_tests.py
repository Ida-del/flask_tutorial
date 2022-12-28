import os
import flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])
        
    def test_empty_db(self):
        rv = self.app.get('/')
        # The assert method is used to check if the response is correct.
        # The response is a string that contains the HTML code of the page.
        # This is the message that is shown when there are no entries in the database.
        assert 'No entries here so far' in rv.data  

if __name__ == '__main__':
    unittest.main()