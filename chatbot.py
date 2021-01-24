import os

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

chilljoy = ChatBot(name = "Chilljoy", read_only = False, logic_adapters = ["chatterbot.logic.BestMatch"], storage_adapter = "chatterbot.storage.SQLStorageAdapter")
while True:
    user_input = input()

    if (user_input == 'quit'):
        break

    response = chilljoy.get_response(user_input)
    print(response)