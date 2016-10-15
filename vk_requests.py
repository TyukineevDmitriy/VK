import requests
import aiohttp
import asyncio
from math import ceil
#from models import *

#mhi = 91925201
#iit = 30390813

class Vk_requests:

    def __init__(self):
        self.__session = aiohttp.ClientSession()
        self.__loop = asyncio.get_event_loop()

    def get_members(self):
        members = requests.get("https://api.vk.com/method/groups.getMembers",
                           params={"group_id":30390813,"fields":{"n"},"v":5.57}).json()['response']['items']
        for member in members:
            if 'deactivated' in member:
                members.remove(member)
        return members


    async def __get_friends(self, member):
        async with self.__session.get('https://api.vk.com/method/friends.get',
                               params={"user_id":member['id'],"fields":"photo_200,photo_100","v":5.57}) as resp:
            friends = (await resp.json())['response']['items']
            accessable_friends = []
            for friend in friends:
                if 'deactivated' not in friend and 'hidden' not in friend:
                    accessable_friends.append(friend)
            member_friends = {}
            member_friends[member['id']] = accessable_friends

            return member_friends

    async def __get_all_friends(self, members):
        tasks = []
        for member in members:
            task = asyncio.ensure_future(self.__get_friends(member))
            tasks.append(task)
        friends_tasks = await asyncio.gather(*tasks)
        friends = {}
        for f in friends_tasks:
            friends.update(f)
        return friends

    def get_all_friends_async(self, members):
        return self.__loop.run_until_complete(asyncio.ensure_future(self.__get_all_friends(members)))

    async def __get_user_posts(self, friend, offset):
        async with self.__session.get('https://api.vk.com/method/wall.get',
                                   params={"owner_id":friend['id'],"fields":{"n"},
                                           "v":5.57,"filter":"owner", "offset":offset, "count": 100}) as resp:
            return (await resp.json())['response']['items']

    async def __get_all_user_posts(self, friend):
        user_posts = []
        async with self.__session.get('https://api.vk.com/method/wall.get',
                                   params={"owner_id":friend['id'],"filter":"owner","fields":{"n"},"v":5.57}) as count:
            count = ceil((await count.json())['response']['count'] / 100)
        for i in range(ceil(count)):
            task = asyncio.ensure_future(self.__get_user_posts(friend, i*100))
            user_posts.append(task)
        tasks = await asyncio.gather(*user_posts)
        wall = []
        for task in tasks:
            wall.extend(task)
        user_posts = {"id":friend["id"],"first_name":friend["first_name"], "last_name":friend["last_name"],
                      "avatar":friend["photo_100"],"wall": wall}
        return user_posts

    async def __get_friends_posts(self, friends):
        friends_posts = []
        for friend in friends:
            task = asyncio.ensure_future(self.__get_all_user_posts(friend))
            friends_posts.append(task)
        return await asyncio.gather(*friends_posts)

    def get_friends_posts_async(self, friends):
        return self.__loop.run_until_complete(asyncio.ensure_future(self.__get_friends_posts(friends)))

    def __del__(self):
        self.__session.close()

    """async def get_all_posts(friends):
        async with aiohttp.ClientSession(loop=loop) as session:
            posts = []
            for member in friends:
                posts.append(await get_friends_posts(session, member))
            return posts"""
