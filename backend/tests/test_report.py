import unittest
from io import BytesIO
from flask import request, current_app
import sys
sys.path.append('../')
from app import app, db
from app import User, Event
from routes import generate_report, generate_pdf_report
from reportlab.pdfgen import canvas

class ReportTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test context."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.client = app.test_client()
        with app.app_context():
            db.create_all()

            # Create test data
            user1 = User(fullname="John Doe", email="john@example.com", password="securepassword")
            user2 = User(fullname="Jane Smith", email="jane@example.com", password="securepassword2")
            event1 = Event(name="Charity Run", date="2024-11-20", location="Park", description="Run for a cause")
            event2 = Event(name="Food Drive", date="2024-12-01", location="Community Center", description="Help distribute food")

            user1.events.append(event1)
            db.session.add_all([user1, user2, event1, event2])
            db.session.commit()

    @classmethod
    def tearDownClass(cls):
        """Clean up the test database."""
        with app.app_context():
            db.drop_all()

    def test_generate_report_invalid_type(self):
        """Test generate_report with an invalid report type."""
        response = self.client.get('/api/generate_report?type=invalid')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid report type', response.data)

    def test_generate_report_pdf(self):
        """Test generate_report for PDF generation."""
        response = self.client.get('/api/generate_report?type=pdf')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/pdf')

    def test_generate_pdf_report(self):
        """Test the generate_pdf_report function directly."""
        with app.app_context():
            response = generate_pdf_report()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.mimetype, 'application/pdf')

    def test_wrap_text(self):
        """Test the wrap_text helper function."""
        text = "This is a long string that should be wrapped properly."
        max_width = 100

        # Simulate ReportLab canvas to measure string width
        canvas_obj = canvas.Canvas(BytesIO())
        wrapped_lines = generate_pdf_report.wrap_text(text, max_width)

        # Test: Check if the text is wrapped into multiple lines
        for line in wrapped_lines:
            self.assertLessEqual(canvas_obj.stringWidth(line, "Helvetica", 10), max_width)

    def test_generate_report_csv(self):
        """Test generate_report for CSV generation."""
        response = self.client.get('/api/generate_report?type=csv')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/csv')
        self.assertIn(b'Volunteer', response.data)

if __name__ == '__main__':
    unittest.main()
