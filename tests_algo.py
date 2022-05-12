import unittest
from run import app
# set our application to testing mode
from model.load import predict
from werkzeug.utils import secure_filename
from app.admin.forms import ImgForm
import os
app.testing = True


class TestAlgo(unittest.TestCase):

    def test_prediction_algo(self):
        form = ImgForm()
        tester = app.test_client(self)
        filename = secure_filename(form.file.data.filename)
        prediction = predict(os.path.join('app/static/uploads/', filename))
        response = tester.get('/images/add', data=dict(prediction=prediction[0]))
        self.assertEqual(response)


    def test_performance_algo(self):
        form = ImgForm()
        tester = app.test_client(self)
        filename = secure_filename(form.file.data.filename)
        prediction = predict(os.path.join('app/static/uploads/', filename))
        response = tester.get('/images/add', data=dict(out=prediction[1]))
        self.assertEqual(response)


if __name__ == '__main__':
    unittest.main()

