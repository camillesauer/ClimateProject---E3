# tests.py
import unittest
from flask_testing import TestCase
from model.load import predict
from app import create_app, db
from werkzeug.utils import secure_filename
from app.admin.forms import ImgForm
from app.models import User
import os

class TestAlgo(TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql+pymysql://student:PanapoiC19!@localhost/climatedb'
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """

        db.create_all()

        # create test admin user
        admin = User()
        admin.username = "admin2"
        admin.password = "admin2016"
        admin.is_admin = True

        # create test non-admin user
        user = User()
        user.username = "test_user"
        user.password = "test2016"

        # save users to database
        db.session.add(admin)
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()

    # tests.py

    def test_prediction_algo(self):

        form = ImgForm()
        if form.validate_on_submit():
            filename = secure_filename(form.file.data.filename)
            prediction = predict(os.path.join('app/static/uploads/', filename))
            response = self.client.get('/images/add', data=dict(prediction=prediction[0]))
            self.assertEqual(response, 0)


    def test_performance_algo(self):
        form = ImgForm()
        if form.validate_on_submit():
            filename = secure_filename(form.file.data.filename)
            prediction = predict(os.path.join('app/static/uploads/', filename))
            response = self.client.get('/images/add', data=dict(out=prediction[1]))
            self.assertEqual(response, 0)

if __name__ == '__main__':
    unittest.main()