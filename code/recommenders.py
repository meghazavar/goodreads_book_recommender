
# Import libraries here.
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
lemmatizer = WordNetLemmatizer()
from sklearn.metrics.pairwise import pairwise_distances
import regex as re
from scipy import sparse
import pickle
#--------------------------------------------
class  helper:
    def __init__(self,_ds):
        print("in constructor collab_recommender")
        self.ds =_ds

    def search_by_title(self,title,strict =True):
        if(strict ==True):
          print(self.ds.loc[self.ds['title'].str.lower().str.contains(title.lower()),['title','book_id']])
          return
        arr = title.split(' ')
        for a in arr:
          print(self.ds.loc[self.ds['title'].str.lower().str.contains(a.lower()),['title','book_id']])

    def book_cluster(self,book_id):
        return ds.loc[ds['book_id'] == book_id,'Cluster'].values[0]

    def book_title(self,book_id):
        return self.ds.loc[self.ds['book_id'] == book_id,'title'].values[0]

    def book_author(self,book_id):
        return ds.loc[ds['book_id'] == book_id,'authors'].values[0]

    def book_goodreads_book_id(self,book_id):
        return ds.loc[ds['book_id'] == book_id,'goodreads_book_id'].values[0]

class content_recommender:
    """docstring for ."""

    def __init__(self):
        print("in constructor content_recommender")

    def book_title(self,ds,book_id):
        return self.ds.loc[self.ds['book_id'] == book_id,'title'].values[0]

    def build_nlp_content_recommender(self,ds, column):
        tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
        tfidf_matrix = tf.fit_transform(ds[column])
        cosine_similarities = cosine_similarity(tfidf_matrix,tfidf_matrix)
        return cosine_similarities

    def create_bag_of_words(self,msg):
        letters_only = re.sub("[^a-zA-Z]", " ", msg) # Remove non-letters.
        words = letters_only.lower().split()  #Convert to lower case, split into individual words.
        ps= PorterStemmer()
        base_words =[ps.stem(w) for w  in words]
        return(" ".join(base_words))# 6. Join the words back into one string separated by space,

    def build(self,ds, column):
        print(f"builing content recommender using {column}...")
        ds[column] =ds[column].apply(self.create_bag_of_words)
        cosine_similarities =self.build_nlp_content_recommender(ds,column)
        pickle.dump(cosine_similarities, open('content_cs.p', 'wb'))
        return cosine_similarities

    def recommend(self,ds,book_id,cosine_similarities):
        author =ds[ds['book_id'] ==book_id]['authors'].values[0]
        title =ds[ds['book_id'] ==book_id]['title'].values[0]

        idx =ds.index[ds['book_id'] ==book_id].values[0]
        closet_match_indices = cosine_similarities[idx].argsort()[:-5:-1]
        similar_items = [(np.round(cosine_similarities[idx][i],2), ds['book_id'][i],book_id) for i in closet_match_indices]

        #print(f"||=>{title}| {author} | {book_id}|  ")
        abc= "|Content |"
        i=0
        for rec in similar_items:
            if(0.1 <= rec[0] < 1):
                i=i+1
                book_id = rec[1]
                print(book_id)
                title = ds.loc[books['book_id'] == book_id,'title'].values[0]
                abc = abc + (f"{title}")

        print(f"||=>{title}| {author} | {book_id}|  ")
        print(abc)

class collab_recommender:
    """docstring for ."""

    def __init__(self,books,ratings):
        print("in constructor collab_recommender")
        self.df =pd.merge(books[['book_id','title']],ratings, how ='inner',left_on ='book_id',right_on='book_id')

    def build_item_based(self):
        pivot =self.df.pivot_table(index ='title',columns ='user_id',values='rating')
        pivot_sparse = sparse.csr_matrix(pivot.fillna(0))
        recommender =pairwise_distances(pivot_sparse,metric='cosine')
        self.recommender_df = pd.DataFrame(recommender , index =pivot.index,columns =pivot.index)
        return self.recommender_df

    def recommend(self,books,book_id, n=3):
        title = books.loc[books['book_id'] == book_id,'title'].values[0]
        print (self.recommender_df[title].sort_values()[1:n+1].index.to_list())

books = pd.read_csv("../data/books_desc.csv")
ratings = pd.read_csv("../data/ratings.csv")


#books['title_description'] = books['authors'] + " " + books['title'] + " " + books['description']
#books.to_csv("../data/books_desc.csv", index=False)

#r_content.build(books,'title_description')

# r_content =content_recommender()
# cs =pickle.load(open('content_cs.p','rb'))
# r_content.recommend(books,1273,cs)

# r_collab =collab_recommender(books,ratings)
# r_collab.build_item_based()
# r_collab.recommend(books,5)

h = helper(books)
print(h.search_by_title('Harry potter',False))
