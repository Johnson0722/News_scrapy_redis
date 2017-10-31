import pickle

with open('content_index.pkl','rb') as f2:
    content_index = pickle.load(f2)
    news_id = pickle.load(f2)

print(news_id)