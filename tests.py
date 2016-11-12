import unittest
from vk_client import *

class TestStringMethods(unittest.TestCase):

    __I = 56783288

    def test_Get_members_Return_good_members(self):
        vk_requests = Vk_requests()
        members = vk_requests.get_members()
        self.assertEqual(members[0]["first_name"], "Владимир")
        self.assertEqual(members[0]["last_name"], "Поляков")

    def test_Get_friends_posts_async_Good_id_Return_good_wall(self):
        newsticker = Newsticker(self.__I)
        self.assertGreater(len(newsticker.newsticker),0)
        newsticker.sort_by_likes()
        self.assertEqual(newsticker.newsticker[0]["text"],
                         "У каждого футболиста есть девушка, но не у каждой девушки есть футболист…")



if __name__ == '__main__':
    unittest.main()