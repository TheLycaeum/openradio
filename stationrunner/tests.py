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
        
        
        
