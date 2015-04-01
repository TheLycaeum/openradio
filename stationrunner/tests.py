from django.test import TestCase
from django.core.urlresolvers import reverse


class TestStationCreate(TestCase):
    def test_page_exists(self):
        """
        Tests if a page exists for creation of station
        """
        response = self.client.get(reverse("createstation"))
        assert response.status_code == 200
    def test_contains_required_fields(self):
        """
        Tests if the page for creation of a station contains a form and
        the required fields
        """
        response = self.client.get(reverse("createstation"))
        assert "form" in response.context
        assert "name" in response.content
        assert "address" in response.content
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
        assert "station" in response.context
        s = response.context["station"]
        assert s.name == name
        assert s.address == address

class TestStationEdit(TestCase):
    def test_page_exists(self):
        """
        Tests if a page exists for editing a created station
        """
        name = "examplename"
        address = "exampleaddress"
        response = self.client.post(reverse("createstation"),
                                    {"name": name, "address": address},
                                    follow=True)
        s = response.context["station"]
        response_two = self.client.get(reverse("editstation", kwargs={'id':s.id}))
        assert response_two.status_code == 200        
        
