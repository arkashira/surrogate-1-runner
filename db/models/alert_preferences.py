from sqlalchemy import Column, Integer, String, Float, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class NotificationChannel(Enum):
    EMAIL = 'email'
    SMS = 'sms'
    WEBHOOK = 'webhook'

class AlertPreference(Base):
    __tablename__ = 'alert_preferences'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    threshold_type = Column(Enum('percentage', 'absolute'), nullable=False)
    threshold_value = Column(Float, nullable=False)
    notification_channel = Column(Enum(NotificationChannel), nullable=False)
    active = Column(Boolean, default=True)

    user = relationship("User", back_populates="alert_preferences")

    def __repr__(self):
        return f"<AlertPreference(id={self.id}, user_id={self.user_id}, threshold_type={self.threshold_type}, threshold_value={self.threshold_value}, notification_channel={self.notification_channel})>"

# /opt/axentx/surrogate-1/db/models/user.py
from sqlalchemy import Column, Integer, String
from .base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    alert_preferences = relationship("AlertPreference", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

# /opt/axentx/surrogate-1/tests/test_alert_preferences.py
import unittest
from db.models.alert_preferences import AlertPreference, NotificationChannel
from db.models.user import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)

class TestAlertPreferences(unittest.TestCase):

    def setUp(self):
        self.session = Session()
        User.__table__.create(engine)
        AlertPreference.__table__.create(engine)

    def tearDown(self):
        User.__table__.drop(engine)
        AlertPreference.__table__.drop(engine)
        self.session.close()

    def test_create_alert_preference(self):
        user = User(username='testuser', email='test@example.com')
        self.session.add(user)
        self.session.commit()

        alert_preference = AlertPreference(
            user_id=user.id,
            threshold_type='percentage',
            threshold_value=10.5,
            notification_channel=NotificationChannel.EMAIL
        )
        self.session.add(alert_preference)
        self.session.commit()

        retrieved_preference = self.session.query(AlertPreference).first()
        self.assertEqual(retrieved_preference.user_id, user.id)
        self.assertEqual(retrieved_preference.threshold_type, 'percentage')
        self.assertEqual(retrieved_preference.threshold_value, 10.5)
        self.assertEqual(retrieved_preference.notification_channel, NotificationChannel.EMAIL)

if __name__ == '__main__':
    unittest.main()