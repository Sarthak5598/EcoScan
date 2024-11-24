import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from unittest.mock import patch, MagicMock
from caremi.models import UploadedImage, UserActivity, Tokens, Voucher, UserVoucher
from django.utils import timezone

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def create_user(db):
    def _create_user(username, password, role='client'):
        user = User.objects.create_user(username=username, password=password)
        user.role = role  # Assume role is stored as a user attribute
        user.save()
        return user
    return _create_user

@pytest.fixture
def login_user(client, create_user):
    def _login_user(username, password, role='client'):
        user = create_user(username, password, role)
        client.login(username=username, password=password)
        return user
    return _login_user

### Test for `home` view
def test_home_view(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'caremi/newhome.html' in [t.name for t in response.templates]

### Test for `login_page` view
def test_login_page_view_get(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200
    assert 'caremi/login.html' in [t.name for t in response.templates]

def test_login_page_view_post(client, create_user):
    user = create_user('testuser', 'testpassword')
    response = client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 302  # Redirect after login
    assert response.url == reverse('donate')  # Assuming redirect for 'client'

### Test for `logoutUser` view
def test_logout_user(client, login_user):
    user = login_user('testuser', 'testpassword')
    response = client.get(reverse('logout'))
    assert response.status_code == 302
    assert response.url == reverse('login')

def test_upload_image_view_limit(client, login_user):
    user = login_user('testuser', 'testpassword')
    UserActivity.objects.create(user=user, daily_uploads_count=20, last_activity=timezone.now())
    response = client.post(reverse('upload_image'), {'title': 'Exceeding Limit'})
    assert response.status_code == 200
    assert 'Daily upload limit reached' in response.content.decode()

### Test for `client_side` view
def test_client_side_view_get(client, login_user):
    user = login_user('employeeuser', 'testpassword', role='employee')
    response = client.get(reverse('client_side'))
    assert response.status_code == 200
    assert 'caremi/employee_dashboard.html' in [t.name for t in response.templates]

### Test for `user_dashboard` view
def test_user_dashboard_view(client, login_user):
    user = login_user('testuser', 'testpassword')
    UploadedImage.objects.create(user=user, status='approved', emission=10)
    Tokens.objects.create(user=user, token=50)
    response = client.get(reverse('user_dashboard'))
    assert response.status_code == 200
    assert 'caremi/user_dashboard.html' in [t.name for t in response.templates]
    assert 'username' in response.context
    assert response.context['tokens'] == 50

### Test for `voucher_list` view
def test_voucher_list_view(client, login_user):
    user = login_user('testuser', 'testpassword')
    Tokens.objects.create(user=user, token=50)
    Voucher.objects.create(name="Test Voucher", token_cost=10, is_active=True)
    response = client.get(reverse('voucher_list'))
    assert response.status_code == 200
    assert 'caremi/voucher_list.html' in [t.name for t in response.templates]
    assert len(response.context['vouchers']) == 1