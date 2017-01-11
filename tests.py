import unittest
from unittest.mock import patch

from client.vk_client import *


class VKRequestTestCase(unittest.TestCase):

    __test_users = [{'first_name': 'Ксения',
                       'photo_100': 'https://pp.vk.me/c629403/v629403353/a1e9/GE-8dT6j584.jpg',
                       'id': 10950353, 'last_name': 'Туманова'}]
    __test_posts = [{'text': 'Никогда раньше не слышал настолько крутых греков. Именно эта вещь вкатывает особенно '
                             'сильно со второй минуты, где соло появляется. А на отметке 3:10 начинается вторая волна'
                             ' кача.',
                     'attachments': [{'audio': {'artist': 'Rotting Christ', 'owner_id': 2000018811,
                                                'url': 'https://vk.com/mp3/audio_api_unavailable.mp3',
                                                'date': 1409689449, 'id': 304173431, 'genre_id': 18,
                                                'title': "P'unchaw kachun- Tuta kachun", 'duration': 284},
                                      'type': 'audio'}], 'owner_id': 5982250,
                     'reposts': {'count': 0}, 'from_id': 5982250, 'date': 1809689449, 'likes': {'count': 1}, 'id': 8541,
                     'comments': {'count': 1}, 'post_type': 'post'}]

    @patch.object(VKRequests, 'get_members', return_value=__test_users)
    def test_get_members(self, mock_get_members):
        vk_client = VKClient(None)
        members = vk_client.get_members()
        self.assertIsInstance(members[0], User)
        self.assertEqual(members[0].first_name, 'Ксения')

    @patch.object(VKRequests, 'get_friends', return_value=__test_users)
    def test_get_friends(self, mock_get_friends):
        vk_client = VKClient(None)
        friends = vk_client.get_friends(None)
        self.assertIsInstance(friends['friends'][0], User)
        self.assertEqual(friends['friends'][0].first_name, 'Ксения')

    @patch.object(VKRequests, 'get_friends', return_value=__test_users)
    @patch.object(VKRequests, 'get_posts', return_value=__test_posts)
    def test_get_posts(self, mock_get_friends, mock_get_posts):
        vk_client = VKClient(None)
        posts = vk_client.get_posts(None)
        self.assertIsInstance(posts[0], Post)
        self.assertEqual(posts[0].user_id, 5982250)

if __name__ == '__main__':
    unittest.main()