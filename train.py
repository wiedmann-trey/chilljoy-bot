import os

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer


chilljoy = ChatBot(name = "Chilljoy", read_only = False, logic_adapters = ["chatterbot.logic.BestMatch"], storage_adapter = "chatterbot.storage.SQLStorageAdapter")

corpus_trainer = ChatterBotCorpusTrainer(chilljoy)

for filename in os.listdir("english"):
    print(filename)
    corpus_trainer.train("english/" + filename)