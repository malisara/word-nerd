from django.urls import reverse


def register_user(client,
                  username='testuser1',
                  password='coolpassyow1',
                  password2='coolpassyow1',):
    data_register = {'username': username,
                     'password': password, 'password2': password2}
    return client.post(reverse('register'), data_register, format='json')


def register_and_login_user(client,
                            username='testuser1',
                            password='coolpassyow1'):
    register_user(client, username, password)
    data_login = {'username': username,
                  'password': password}
    login_response = client.post(reverse('login'), data_login, format='json')
    client.credentials(HTTP_AUTHORIZATION='Token ' +
                       login_response.data['token'])
    return login_response
