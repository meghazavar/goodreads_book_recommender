#!/usr/bin/env python3
import pandas as pd
import numpy as np
from betterreads import client
import os

class  helper:


    def __init__(self):
        print("Gathering data... ")
        self.gc = client.GoodreadsClient('zIHHGGHATvYay6dTTZ1AqA',
                            'xFiCr7PBabSezd7zpXhqNyvsIDFfoX4ftC6Pww7v2g')

    def get_book(self,goodreads_book_id):
        book = self.gc.book(goodreads_book_id)
        return book

    def get_book_id_list_for_missing_column(self,books,column):
        books[column].isna().sum()
        missing_desc_books = books[books[column].isna()]['book_id'].values
        return missing_desc_books

    def fill_missing_columns(self,fname,howmany='all'):
        books =pd.read_csv("../data/books_desc.csv")
        missing_desc_books = self.get_book_id_list_for_missing_column(books,'description')
        print(missing_desc_books)
        print (f"getting {howmany} out of missing {len(missing_desc_books)} descriptions" )
        howmany = len(missing_desc_books) if(howmany =='all') else howmany

        for i in missing_desc_books[ :howmany]:
            goodreads_book_id = books.loc[books['book_id'] == i,'goodreads_book_id'].values[0]

            try:
                book_obj= h.get_book(goodreads_book_id)

                print( f"{i},{book_obj}")
                if(i % 10 ==0):
                    print("saving the results to the file....")
                    books.to_csv(fname, index=False)

                books.loc[books['book_id'] == i,'description']= book_obj.description
                try:
                    books.loc[books['book_id'] == i,'num_pages']=  book_obj.num_pages
                except:
                    books.loc[books['book_id'] == i,'num_pages']=  0

                books.loc[books['book_id'] == i,'is_ebook']=book_obj.is_ebook
            except:
                #print(exp)
                books.loc[books['book_id'] == i,'num_pages']=  0
                books.loc[books['book_id'] == i,'description'] =""
                books.loc[books['book_id'] == i,'is_ebook'] =False
                #print(f"failed to parse {i}")
        return books

    def get_books(self,topic, strict =True):
        books_on_subject = self.gc.search_books(topic)
        books_list =[]
        for b in books_on_subject:
           try:
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
               if((strict== True) and (b.isbn is not None) and (b.description is not None) and (b.average_rating is not None)):
                   books_list.append(book)
                   print(f"Downloading book {b.title} for topic {topic}")
               elif (strict== False):
                   books_list.append(book)
                   print(f"Downloading book {b.title} for topic {topic}")
           except:
                print(f"failed to parse {b.title}")
        df =pd.DataFrame(books_list)
        return df


h=helper()
h.fill_missing_columns("../data/books_desc.csv",1000)
