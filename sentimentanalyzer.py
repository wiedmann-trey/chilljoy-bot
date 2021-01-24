
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier

import re, string, random

random.seed(420)

def cleanup(tweet_tokens, stop_words = ()):

    ctokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        
        elif tag.startswith("VB"):
            pos = 'v'

        else:
            pos = 'a'
        

        lemmatizer = WordNetLemmatizer()

        token = lemmatizer.lemmatize(token, pos)

        if (len(token) > 0) and (token not in string.punctuation) and (token.lower() not in stop_words):
            ctokens.append(token.lower())

    
    return ctokens

def getwords(ctlist):
    for tokens in ctlist:
        for token in tokens:
            yield token

def gettweets(ctlist):
    for ttokens in ctlist:
        yield dict([token, True] for token in ttokens)

positive_tweets = twitter_samples.strings('positive_tweets.json')
negative_tweets = twitter_samples.strings('negative_tweets.json')
text = twitter_samples.strings('tweets.20150430-223406.json')
tweet_tokens = twitter_samples.tokenized('positive_tweets.json')[0]

stop_words = stopwords.words('english')

positive_tokens = twitter_samples.tokenized('positive_tweets.json')
negative_tokens = twitter_samples.tokenized('negative_tweets.json')

positive_ctokens = []
negative_ctokens = []

for tokens in positive_tokens:
    positive_ctokens.append(cleanup(tokens, stop_words))

for tokens in negative_tokens:
    negative_ctokens.append(cleanup(tokens, stop_words))

all_pos_tags = getwords(positive_ctokens)

fdist_pos = FreqDist(all_pos_tags)

print(fdist_pos.most_common(10))

model_ready_ptokens = gettweets(positive_ctokens)
model_ready_ntokens = gettweets(negative_ctokens)

p_dataset = [(tweet, "Positive") for tweet in model_ready_ptokens]
n_dataset = [(tweet, "Negative") for tweet in model_ready_ntokens]

dataset = p_dataset + n_dataset

random.shuffle(dataset)

train_data = dataset[:7000]
test_data = dataset[7000:]

classifier = NaiveBayesClassifier.train(train_data)

print("Accuracy: ", classify.accuracy(classifier, test_data))


my_tweet = "I wish that I could be eating pancakes right now."
my_tokens = cleanup(word_tokenize(my_tweet))

print(my_tweet, classifier.classify(dict([token, True] for token in my_tokens)))
