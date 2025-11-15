from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Game

class UserAndGameTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.game = Game.objects.create(
            owner=self.user,
            title='Test Game',
            platform='PC',
            status='playing',
            rating=5
        )

    def test_register_view(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass',
            'password2': 'newpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('logout_handler'))
        self.assertEqual(response.status_code, 302)

    def test_game_list_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Game')

    def test_add_game(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('add_game'), {
            'title': 'New Game',
            'platform': 'PC',
            'status': 'wishlist',
            'rating': 4
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Game.objects.filter(title='New Game').exists())

    def test_edit_game(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('edit_game', args=[self.game.id]), {
            'title': 'Edited Game',
            'platform': 'PC',
            'status': 'completed',
            'rating': 5
        })
        self.assertEqual(response.status_code, 302)
        self.game.refresh_from_db()
        self.assertEqual(self.game.title, 'Edited Game')
        self.assertEqual(self.game.status, 'completed')

    def test_delete_game(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('delete_game', args=[self.game.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Game.objects.filter(id=self.game.id).exists())
