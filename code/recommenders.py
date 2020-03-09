
# Import libraries here.
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

class  helper
    def __init__(self):
        print("in constructor collab_recommender")

    def find_titles(self,books, title):
        titles = books.loc[books['title'].str.lower().str.contains(title),'title'].tolist()
        return titles
    def search_by_title(title):
        l= ds.loc[ds['title'].str.lower().str.contains(title),['title','book_id']].tolist()
        return l

    def book_title(book_id):
        return ds.loc[ds['book_id'] == book_id,'title'].values[0]

class collab_recommender:
    """docstring for ."""

    def __init__(self):
        print("in constructor collab_recommender")



class collab_recommender:
    """docstring for ."""

    def __init__(self):
        print("in constructor collab_recommender")

def main():
  print("Hello World!")
  books=  pd.read_csv("../data/books.csv")
  helper = Helper()
  titles = helper.find_titles(books,'positive')
  print(titles)

if __name__ ==  '__main__':
   main()
