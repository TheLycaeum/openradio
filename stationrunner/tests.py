from django.test import TestCase
from django.core.urlresolvers import reverse

# Create your tests here.

class TestStationCreate(TestCase):
    def test_page_exists(self):
        """
        Tests if a page exists for creation of station
        """
        response = self.client.get(reverse("createstation"))
        self.assertEqual(response.status_code, 200)
    def test_contains_required_fields(self):
        """
        Tests if the page for creation of a station contains the required fields
        """
        response = self.client.get(reverse("createstation"))
        self.assertIn("name", response.content)
        self.assertIn("address", response.content)
        
        
        
