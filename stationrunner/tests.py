from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .models import Station
from .models import Channel

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
        name = "anyname"
        address = "anyaddress"
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
        s = Station(name="anyname",address="anyddress")
        s.save()
        response_two = self.client.get(reverse("editstation", kwargs={'pk':s.pk}))
        assert response_two.status_code == 200  
    
    def test_contains_required_fields(self):
        """
        Tests if the page for editing a station contains a form and
        the required fields containing values from the station object to be 
        edited
        """
        s = Station(name="anyname",address="anyddress")
        s.save()
        response_two = self.client.get(reverse("editstation", kwargs={'pk':s.pk}))
        assert "form" in response_two.context
        assert s.name in response_two.content
        assert s.address in response_two.content
        
    def test_submission_form_edits_station_object(self):
        """
        Tests if submission of the form on page for editing an
        existing station object saves the object into db with the
        attributes overwritten with the new values.
        """
        s = Station(name="anyname",address="anyddress")
        s.save()
        response_two = self.client.get(reverse("editstation", kwargs={'pk':s.pk}))                            
        response_three = self.client.post(reverse("editstation", kwargs={'pk':s.pk}),
                                          {"name": "editedname", "address": "editedaddress"},
                                          follow=True)
        edited_s = response_three.context["station"]
        assert edited_s.name == "editedname"
        assert edited_s.address == "editedaddress"
        assert s.id == edited_s.id

class TestListStations(TestCase):
    def test_page_exists(self):
        """
        Checks if a page exists at the desired URL for listing all the
        stations.
        """
        response = self.client.get(reverse("liststations"))
        assert response.status_code == 200
        
    def test_page_lists_stations(self):
        """
        Checks if page for listing all the stations actually lists them
        """
        s1 = Station(name="name1",address="address1")
        s1.save()
        s2 = Station(name="name2",address="address2")
        s2.save()
        s3 = Station(name="name3",address="address3")
        s3.save()
        response = self.client.get(reverse("liststations"),
                                   follow=True)
        assert s1.name in response.content
        assert s1.address in response.content
        assert s2.name in response.content
        assert s2.address in response.content
        assert s3.name in response.content
        assert s3.address in response.content

class TestUserSignUp(TestCase):
    def test_page_exists(self):
        """
        Checks if a page exists at the desired URL for user registration.
        """
        response = self.client.get(reverse("userregistration"))
        assert response.status_code == 200
        
    def test_page_holds_user_object(self):
        """
        Checks if the page for user registration holds an object of
        the User model
        """
        response = self.client.get(reverse("userregistration"))
        assert response.context["user"]

    def test_contains_required_fields(self):
        """
        Tests if the page for user registration contains a form with
        the required fields
        """
        response = self.client.get(reverse("userregistration"))
        assert "form" in response.context
        assert "first_name" in response.content
        assert "last_name" in response.content
        assert "email" in response.content
        assert "username" in response.content
        assert "password1" in response.content #password
        assert "password2" in response.content #password confirmation
    
    def test_submission_form_creates_user_object(self):
        """
        Tests if submission of the form on page for creation of a 
        user creates a user object and its attributes take the 
        expected values
        """
        first_name = "somename"
        last_name = "somename"
        email = "someemail@someservice.com"
        username = "someusername"
        password = "somepassword"
        response = self.client.post(reverse("userregistration"),
                                    {"first_name": first_name,
                                     "last_name": last_name,
                                     "email": email,
                                     "username": username,
                                     "password1": password,
                                     "password2": password},
                                    follow=True)
        assert User.objects.get(username=username)
        user = User.objects.get(username=username)
        
    def test_no_two_users_can_have_same_username(self):
        """
        Tests if duplicate username will be rejected by the page
        """
        first_name1 = "somename"
        last_name1 = "somename"
        email1 = "someemail@someservice.com"
        username1 = "someusername"
        password1 = "somepassword"
        response1 = self.client.post(reverse("userregistration"),
                                    {"first_name": first_name1,
                                     "last_name": last_name1,
                                     "email": email1,
                                     "username": username1,
                                     "password1": password1,
                                     "password2": password1},
                                    follow=True)
        first_name2 = "someothername"
        last_name2 = "someothername"
        email2 = "someotheremail@someservice.com"
        password2 = "someotherpasswordd"
        response2 = self.client.post(reverse("userregistration"),
                                    {"first_name": first_name2,
                                     "last_name": last_name2,
                                     "email": email2,
                                     "username": username1,  # same username
                                     "password1": password2,
                                     "password2": password2},
                                    follow=True)
        users_with_username1 = 0
        for user in User.objects.all():
            if user.username == username1:
                users_with_username1 += 1
        assert users_with_username1 == 1

    def test_no_two_users_can_have_same_email(self):
        """
        Tests if duplicate email will be rejected by the page
        """
        first_name1 = "somename"
        last_name1 = "somename"
        email1 = "someemail@someservice.com"
        username1 = "someusername"
        password1 = "somepassword"
        response1 = self.client.post(reverse("userregistration"),
                                    {"first_name": first_name1,
                                     "last_name": last_name1,
                                     "email": email1,
                                     "username": username1,
                                     "password1": password1,
                                     "password2": password1},
                                    follow=True)
        first_name2 = "someothername"
        last_name2 = "someothername"
        username2 = "someotherusername"
        password2 = "someotherpasswordd"
        response2 = self.client.post(reverse("userregistration"),
                                    {"first_name": first_name2,
                                     "last_name": last_name2,
                                     "email": email1,       # same email
                                     "username": username2, 
                                     "password1": password2,
                                     "password2": password2},
                                    follow=True)
        users_with_email1 = 0
        for user in User.objects.all():
            if user.email == email1:
                users_with_email1 += 1
        assert users_with_email1 == 1
        users_with_email1 = 0
        for user in User.objects.all():
            if user.email == email1:
                users_with_email1 += 1
        assert users_with_email1 == 1
    
    def test_registration_also_signs_user_in(self):
        """
        Assures that registration signs in the user too
        """
        first_name = "somename"
        last_name = "somename"
        email = "someemail@someservice.com"
        username = "someusername"
        password = "somepassword"
        response = self.client.post(reverse("userregistration"),
                                    {"first_name": first_name,
                                     "last_name": last_name,
                                     "email": email,
                                     "username": username,
                                     "password1": password,
                                     "password2": password},
                                    follow=True)
        user = response.context["user"]
        assert user.is_authenticated()
                
class TestChannelCreate(TestCase):
    def test_channel_page_exists(self):
        """
        Tests if channel creation page exists
        """
        response = self.client.get(reverse("createchannel"))
        assert response.status_code == 200

    def test_channel_contains_required_fields(self):
        """
        Tests if the channel page of a channel contains a form and
        the required fields
        """
        response = self.client.get(reverse("createchannel"))
        assert "form" in response.context
        assert "c_name" in response.content
        assert "c_frequency" in response.content

    def test_submission_form_creates_channel_object(self):
        """
        Tests if submission of page form creates a channel object and
        its attributes take the submitted values
        """
        c_name = "anyname"
        c_frequency = "anyaddress"
        response = self.client.post(reverse("createchannel"),
                                    {"c_name": c_name, "c_frequency": c_frequency},
                                    follow=True)
        assert "channel" in response.context
        c = response.context["channel"]
        assert c.c_name == c_name
        assert c.c_frequency == c_frequency


class TestChannelEdit(TestCase):
    def test_channe_page_exists(self):
        """
        Tests if a channel page exists for editing a created channel
        """
        c = Channel(c_name="anyname",c_frequency="anyfrequency")
        c.save()
        response_two = self.client.get(reverse("editchannel", kwargs={'pk':c.pk}))
        assert response_two.status_code == 200

    def test_channel_contains_required_fields(self):
        """
        Tests if the page for editing a channel contains a form and
        the required fields containing values from the channel object to be 
        edited
        """
        c = Channel(c_name="anyname",c_frequency="anyfrequency")
        c.save()
        response_two = self.client.get(reverse("editchannel", kwargs={'pk':c.pk}))
        assert "form" in response_two.context
        assert c.c_name in response_two.content
        assert c.c_frequency in response_two.content

    def test_channel_submission_form_edits_channel_object(self):
        """
        Tests if channel form submission of page for editing an
        existing channel object saves the object in db with
        attributes overwritten.
        """
        c = Channel(c_name="anyname",c_frequency="anyfrequency")
        c.save()
        response_two = self.client.get(reverse("editchannel", kwargs={'pk':c.pk}))                            
        response_three = self.client.post(reverse("editchannel", kwargs={'pk':c.pk}),
                                          {"c_name": "editedname", "c_frequency": "editedfrequency"},
                                          follow=True)
        edited_c = response_three.context["channel"]
        assert edited_c.c_name == "editedname"
        assert edited_c.c_frequency == "editedfrequency"
        assert c.id == edited_c.id

class TestListChannels(TestCase):
    def test_channel_page_exists(self):
        """
        Checks if a page exists at the desired URL for listing all the
        channels
        """
        response = self.client.get(reverse("listchannels"))
        assert response.status_code == 200
