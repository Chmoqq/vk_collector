# -*- coding: utf-8 -*-
import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType

class VKBot:
    last_messages = {}
    phraseList = ["сообщение 1", "сообщение 2", "сообщение 3"]

    login, password = "user_name", "password"
    vk = None
    vk_session = None
    longpoll = None

    def __init__(self):
        self.vk_session = vk_api.VkApi(self.login, self.password)

        try:
            self.vk_session.auth()
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return

        self.longpoll = VkLongPoll(self.vk_session)
        self.vk = self.vk_session.get_api()

    def listen(self):
        print("Waiting for messages..")

        for event in self.longpoll.listen():
            if event.type == VkEventType.USER_ONLINE and event.user_id in ["user_name"]:
                print('Пользователь', event.user_id, 'онлайн', event.platform)
                self.send_random_phrase(event.user_id)

    def send_random_phrase(self, user_id):
        selected_phrase = random.choice(self.phraseList)

        while len(self.phraseList) > 1 and user_id in self.last_messages.keys() and selected_phrase == self.last_messages[user_id]:
            selected_phrase = random.choice(self.phraseList)

        self.vk.messages.send(user_id=user_id, message=selected_phrase)

if __name__ == "__main__":
    bot = VKBot()

    bot.listen()