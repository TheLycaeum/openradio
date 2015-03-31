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
        Tests if the page for creation of a station contains a form and
        the required fields
        """
        response = self.client.get(reverse("createstation"))
        self.assertIn("form", response.context)
        self.assertIn("name", response.content)
        self.assertIn("address", response.content)
    def test_submission_form_creates_station_object(self):
        """
        Tests if submission of the form on page for creation of a 
        station creates a station object and its attributes take the 
        submitted values
        """
        name = "examplename"
        address = "exampleaddress"
        response = self.client.post(reverse("createstation"),
                                    {"name": name, "address": address},
                                    follow=True)
        self.assertIn("station", response.context)
        s = response.context["station"]
        s.name = name
        s.address = address

        
        
        
        
