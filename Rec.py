import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
ds = pd.read_csv("/Users/anudeep/Documents/GitHub/InternProject2018/movie.csv")
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 10), min_df=0, stop_words='english')

tfidf_matrix = tf.fit_transform(ds['genres'])
cosine_similarities = cosine_similarity(tfidf_matrix,tfidf_matrix)

results = {} # Dictionary of result with (Score and Item ID)

for idx, row in ds.iterrows(): #iterates through all the rows
    similar_indices = cosine_similarities[idx].argsort()[:-12:-1] #[:number:-1] 'number' shoud always be greater than b in recommend(a,b) by 2 points.
    similar_items = [(cosine_similarities[idx][i], ds['movieId'][i]) for i in similar_indices]
    results[row['movieId']] = similar_items[1:]
    
def item(id):
    return ds.loc[ds['movieId'] == id]['title'].tolist()[0]
def recommend(id, num):
    if (num == 0):
        print("Unable to recommend any movie as you have not chosen the number of book to be recommended")
    elif (num==1):
        print("Recommending movie(s) similar to " + item(id))
        
    else :
        print("Recommending movie(s) similar to " + item(id))
        
    print("----------------------------------------------------------")
    recs = results[id][:num]
    for rec in recs:
        if (rec[0] != 0):
            print("You may also like to watch: " + item(rec[1]) + " (score:" + str(rec[0]) + ")")
            
recommend(168250,10) # (Movie ID, Max 10 recs)