from django.test import TestCase
from django.http import HttpRequest
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Station
from .models import Channel


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

 #class TestChannelCreate(TestCase):
 #    def test_channel_page_exists(self):
 #        """
 #        Tests if channel creation page exists
 #        """
 #        response = self.client.get(reverse("createchannel"))
 #       assert response.status_code == 200
 #
 #    def test_channel_contains_required_fields(self):
 #        """
 #        Tests if the channel page of a channel contains a form and
 #        the required fields
 #        """
 #        response = self.client.get(reverse("createchannel"))
 #        assert "form" in response.context
 #        assert "c_name" in response.content
 #        assert "c_frequency" in response.content

 #    def test_submission_form_creates_channel_object(self):
 #        """
 #        Tests if submission of page form creates a channel object and
 #        its attributes take the submitted values
 #        """
 #       c_name = "anyname"
 #        c_frequency = "anyaddress"
 #        response = self.client.post(reverse("createchannel"),
 #                                    {"c_name": c_name, "c_frequency": c_frequency},
 #                                    follow=True)
 #        assert "channel" in response.context
 #        c = response.context["channel"]
 #        assert c.c_name == c_name
 #        assert c.c_frequency == c_frequency


 #class TestChannelEdit(TestCase):
 #    def test_channe_page_exists(self):
 #        """
 #        Tests if a channel page exists for editing a created channel
 #        """
 #        c = Channel(c_name="anyname",c_frequency="anyfrequency")
 #        c.save()
 #        response_two = self.client.get(reverse("editchannel", kwargs={'pk':c.pk}))
 #        assert response_two.status_code == 200

 #    def test_channel_contains_required_fields(self):
 #        """
 #        Tests if the page for editing a channel contains a form and
 #        the required fields containing values from the channel object to be 
 #        edited
 #        """
 #        c = Channel(c_name="anyname",c_frequency="anyfrequency")
 #        c.save()
 #        response_two = self.client.get(reverse("editchannel", kwargs={'pk':c.pk}))
 #        assert "form" in response_two.context
 #        assert c.c_name in response_two.content
 #        assert c.c_frequency in response_two.content

 #    def test_channel_submission_form_edits_channel_object(self):
 #        """
 #        Tests if channel form submission of page for editing an
 #        existing channel object saves the object in db with
 #        attributes overwritten.
 #        """
 #       c = Channel(c_name="anyname",c_frequency="anyfrequency")
 #        c.save()
 #        response_two = self.client.get(reverse("editchannel", kwargs={'pk':c.pk}))                            
 #        response_three = self.client.post(reverse("editchannel", kwargs={'pk':c.pk}),
 #                                         {"c_name": "editedname", "c_frequency": "editedfrequency"},
 #                                          follow=True)
 #        edited_c = response_three.context["channel"]
 #        assert edited_c.c_name == "editedname"
 #        assert edited_c.c_frequency == "editedfrequency"
 #        assert c.id == edited_c.id

 #class TestListChannels(TestCase):
 #    def test_channel_page_exists(self):
 #        """
 #        Checks if a page exists at the desired URL for listing all the
 #        channels
 #        """
 #        response = self.client.get(reverse("listchannels"))
 #        assert response.status_code == 200

class TestLoginPage(TestCase):
    def test_page_exists(self):
        """
        Tests if a page exist at the desired URL for login
        """
        response = self.client.get(reverse("userlogin"))
        assert response.status_code == 200
        
    def test_page_logs_user_in(self):
        """
        Tests if the login page actually logs a user in
        """
        username = "someusername"
        password = "somepassword"
        user = User.objects.create_user(username=username,
                                        password=password
                                    )
        user.save()
        response = self.client.post(reverse("userlogin"),
                                    {"username":username,
                                     "password":password
                                 },
                                    follow=True
                                )
        assert user.is_authenticated() 
        
    def test_page_redirects_to_user_home_on_login(self):
        """
        Test to assure that the login page redirects to the user's
        home page
        """
        username = "someusername"
        password = "somepassword"
        user = User.objects.create_user(username=username,
                                        password=password)
        user.save()
        response = self.client.post(reverse("userlogin"),
                                    {"username":username,
                                     "password":password,
                                     "next":reverse("userredirect")
                                 },
                                    follow=True
                                )
        assert response.wsgi_request.path == reverse("userhome",
                                                     kwargs={'pk':user.pk}
                                                 )
        

class TestUserHomePage(TestCase):
    def test_uanimous_access_denied(self):
        """
        Assures unanimous user cannot access user home page
        """
        username1="somename"
        password1="somepassword"
        rightful_user = User.objects.create_user(username=username1,
                                                 password=password1,
                                             )
        rightful_user.save()
        username2="someothername"
        password2="someotherpassword"
        unanimous_user = User.objects.create_user(username=username2,
                                                    password=password2,
                                                )
        unanimous_user.save()

        self.client.login(username=username2,
                          password=password2,
        )

        response = self.client.get(reverse('userhome',
                                           kwargs={'pk':rightful_user.pk,
                                               },
                                       )
                               )
        assert response.content.decode() == \
                         render_to_string('deny_user.html')

    def test_rightful_access_not_denied(self):
        """
        Assures rightful user is not denied user home page
        """
        username="somename"
        password="somepassword"
        rightful_user = User.objects.create_user(username=username,
                                                 password=password,
                                             )
        rightful_user.save()

        self.client.login(username=username,
                          password=password,
        )
        response = self.client.get(reverse('userhome',
                                   kwargs={'pk':rightful_user.pk,
                                       },
                                       )
                               )
        assert response.content.decode() != \
            render_to_string('deny_user.html')
                    
    def test_no_access_without_login(self):
        """
        Assures login required for access
        """
        
        username="somename"
        password="somepassword"
        user = User.objects.create_user(username=username,
                                        password=password,
                                             )
        user.save()
        response = self.client.get(reverse('userhome',
                                           kwargs={'pk':user.pk,
                                               },
                                       ),
                                   follow =True,
                               )
        assert response.wsgi_request.path == reverse('userlogin')
        
class TestStationListCreate(TestCase):
    def test_authentication(self):
        """
        This assures that page for stations is accessible only
        on login.
        """
        response = self.client.get(reverse('list_create_station'),
                                   follow=True,
        )
        assert response.wsgi_request.path == reverse('userlogin')
    
    def test_stations_under_user_listed(self):
        """
        Assures list of stations contains stations created by
        logged in user
        """
        username = "somename"
        password = "somepassword"
        user = User.objects.create_user(username=username,
                                        password=password,
                                    )
        user.save()
        station1 = Station.objects.create(name="somename",
                               address="someaddres",
                               owner=user
                               )
        station1.save()
        station2 = Station.objects.create(name="someothername",
                               address="someotheraddres",
                               owner=user
                               )
        station2.save()

        self.client.login(username=username,password=password)
        response = self.client.get(reverse('list_create_station'))
        assert station1 in response.context['stations']
        assert station2 in response.context['stations']
        

    def test_stations_under_different_user_not_listed(self):
        """
        Assures list of stations does not contain stations
        not created by logged in user.
        """
        username1 = "somename"
        password1 = "somepassword"
        user1 = User.objects.create_user(username=username1,
                                        password=password1,
                                    )
        user1.save()
        username2 = "someothername"
        password2 = "someotherpassword"
        user2 = User.objects.create_user(username=username2,
                                        password=password2,
                                    )
        user2.save()
        station1 = Station.objects.create(name="somename",
                               address="someaddres",
                               owner=user1
                               )
        station1.save()
        station2 = Station.objects.create(name="someothername",
                               address="someotheraddres",
                               owner=user1
                               )
        station2.save()
 
        self.client.login(username=username2,password=password2)
        response = self.client.get(reverse('list_create_station'))
        assert station1 not in response.context['stations']
        assert station2 not in response.context['stations']

class TestStationHome(TestCase):        
    def test_login_required(self):
        """
        Assures page demands user be logged in
        """
        username="someusername"
        password="somepassword"
        user = User.objects.create_user(
            username=username,
            password=password
        )
        user.save()
        station = Station.objects.create(
            name="somename",
            address="someaddress",
            owner=user
            )
        station.save()
        response = self.client.get(reverse('home_station',
                                        kwargs={'pk':station.pk
                                            }
                                       ),
                                   follow=True
                               )
        assert response.wsgi_request.path == reverse('userlogin')
            
    def test_authentication(self):
        """
        Assures that only the rightful user can access page
        """
        username1="someusername"
        password1="somepassword"
        unanimous_user = User.objects.create_user(
            username=username1,
            password=password1
        )
        unanimous_user.save()
        username2="someothername"
        password2="someotherpassword"
        rightful_user = User.objects.create_user(
            username=username2,
            password=password2
        )
        rightful_user.save()
        station_in_question = Station.objects.create(
            name="somename",
            address="someaddress",
            owner=rightful_user
        )
        
        self.client.login(username=username1,password=password1) 
        response = self.client.get(
            reverse(
                'home_station',
                kwargs={'pk':station_in_question.pk}
            ),
            follow = True
        )
        assert response.content.decode() == \
            render_to_string('deny_user.html')

        self.client.login(username=username2,password=password2) 
        response = self.client.get(
            reverse(
                'home_station',
                kwargs={'pk':station_in_question.pk}
            ),
            follow = True
        )
        assert response.content.decode() != \
            render_to_string('deny_user.html')
        
        
