import os

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()

chilljoy = ChatBot(name = "Chilljoy", read_only = False, logic_adapters = ["chatterbot.logic.BestMatch"], storage_adapter = "chatterbot.storage.SQLStorageAdapter")

corpus_trainer = ChatterBotCorpusTrainer(chilljoy)

for filename in os.listdir("english"):
    print(filename)
    corpus_trainer.train("english/" + filename)

messages = 0
total_score = 0
total_positive = 0
total_negative = 0
total_neutral = 0

while True:
    user_input = input()
    messages += 1
    sent_dict = sid.polarity_scores(user_input)
    score = sent_dict['compound']
    total_score += score
    if score > 0:
        total_positive += 1
    elif score == 0:
        total_neutral += 1
    else:
        total_negative += 1

    if (user_input == 'quit'):
        print("Average Score: ", total_score / messages)
        print("Positive Messages: ", total_positive)
        print("Neutral Messages: ", total_neutral)
        print("Negative Messages: ", total_negative)
        break

    response = chilljoy.get_response(user_input)
    print(response)