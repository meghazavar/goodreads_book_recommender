import pandas as pd
import numpy as np
from betterreads import client
import os

class  helper:


    def __init__(self):
        print("in constructor ")
        self.gc = client.GoodreadsClient('zIHHGGHATvYay6dTTZ1AqA',
                            'xFiCr7PBabSezd7zpXhqNyvsIDFfoX4ftC6Pww7v2g')

    def get_book(self,goodreads_book_id):
        book = self.gc.book(goodreads_book_id)
        return book

    def get_book_id_list_for_missing_column(self,books,column):
        books[column].isna().sum()
        missing_desc_books = books[books[column].isna()]['book_id'].values
        return missing_desc_books

    def get_books(self,topic):
        books_on_subject = self.gc.search_books(topic)
        books_list =[]
        for b in books_on_subject:
           book ={}
           book['goodreads_book_id']=b.gid
           #book['isbn']= b.isbn
           book['authors']=b.authors
           book['title']=b.title
           book['language_code']=b.language_code
           book['average_rating']=b.average_rating
           book['ratings_count']=b.ratings_count
           book[ 'description']=b.description
           try :
               book['num_pages']=b.num_pages
           except:
               book['num_pages'] =0
           book['is_ebook']=b.is_ebook
           if((b.isbn is not None) and (b.description is not None) and (b.average_rating is not None)):
               books_list.append(book)
        df =pd.DataFrame(books_list)
        return df
