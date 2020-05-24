import unittest, os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from app import app, db
from app.models import User, Qset, Question, Multichoice, Attempts, Results

# unittest.TestLoader.sortTestMethodsUsing = None

class UserModelClass(unittest.TestCase):

    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()

        db.create_all()

        # Create 2 test users, one with admin privs
        user1 = User(username='user1', first_name='User1', last_name='Lastname1',
                     email='user1@test.net', is_admin=False)
        db.session.add(user1)
        db.session.commit()

        user2 = User(username='user2', first_name='User2', last_name='Lastname2',
                     email='user2@test.net', is_admin=True)
        db.session.add(user2)
        db.session.commit()

        # Create test question set
        qset1 = Qset(title='Test Qset 1', is_active=True)
        db.session.add(qset1)
        db.session.commit()
        qset2 = Qset(title='Test Qset 2', is_active=False)
        db.session.add(qset2)
        db.session.commit()

        # Create 2 Questions for first Qset
        question_1_qset1 = Question(qset_id=qset1.id, question="This is question 1", is_multichoice=False)
        question_2_qset1 = Question(qset_id=qset1.id, question="This is MC question 2", is_multichoice=True)
        db.session.add(question_1_qset1)
        db.session.add(question_2_qset1)
        db.session.commit()

        # Create the multichoice entries for question_2_qset1, set the second answer as correct
        question_id = question_2_qset1.id
        mc_answer1 = Multichoice(question_id=question_id, answer_selection="This is answer 1, it is wrong", is_correct=False)
        mc_answer2 = Multichoice(question_id=question_id, answer_selection="This is answer 2, it is correct", is_correct=True)
        mc_answer3 = Multichoice(question_id=question_id, answer_selection="This is answer 3, it is wrong", is_correct=False)
        mc_answer4 = Multichoice(question_id=question_id, answer_selection="This is answer 4, it is wrong", is_correct=False)
        db.session.add(mc_answer1)
        db.session.add(mc_answer2)
        db.session.add(mc_answer3)
        db.session.add(mc_answer4)
        db.session.commit()

        # Create an Attempt entry for the user
        attempt = Attempts(qset_id=qset1.id, user_id=user1.id, timestamp=datetime.utcnow())
        db.session.add(attempt)
        db.session.commit()



    def tearDown(self):
        db.session.remove()
        db.drop_all()


    # Test setting and checking user password and whether admin or not
    def test_01_user_access(self):
        # Test setting and getting password hash
        user = User.query.filter_by(username='user1').first()
        user.set_password('testpassword')
        self.assertTrue(user.check_password('testpassword'))
        self.assertFalse(user.check_password('abcdefg'))

        admin = User.query.filter_by(username='user2').first()
        admin.set_password('adminpassword')
        self.assertTrue(admin.check_password('adminpassword'))
        self.assertFalse(admin.check_password('12345678'))

        # Test check_admin()
        self.assertFalse(user.check_admin())
        self.assertTrue(admin.check_admin())


    # Test for the creation of Question sets, their respective questions and multichoice answers
    def test_02_create_questions(self):
        # First get FK of Qsets
        qset1 = Qset.query.get(1)
        qset2 = Qset.query.get(2)

        question_1_qset1 = Question.query.get(1)
        question_2_qset1 = Question.query.get(2)

        # Test FK references between Question and Qset
        self.assertTrue(question_1_qset1.qset_id == qset1.id)
        self.assertTrue(question_2_qset1.qset_id == qset1.id)

        mc_answer1 = Multichoice.query.get(1)
        mc_answer2 = Multichoice.query.get(2)
        mc_answer3 = Multichoice.query.get(3)
        mc_answer4 = Multichoice.query.get(4)

        # Test FK references between Multichoice and Question
        self.assertTrue(mc_answer1.question_id == question_2_qset1.id)
        self.assertTrue(mc_answer2.question_id == question_2_qset1.id)
        self.assertTrue(mc_answer3.question_id == question_2_qset1.id)
        self.assertTrue(mc_answer4.question_id == question_2_qset1.id)



if __name__ == '__main__':
    unittest.main()