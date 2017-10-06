#!/usr/bin/python3
from pymongo import MongoClient
import pandas as pd

mongo = MongoClient()
db = mongo.steemdb

cursor = db.comment.find({
    "depth" : 0.0
}, {
    "body" : 1.0,
    "title" : 1.0
})

comment_df = pd.DataFrame(columns=['title', '_id', 'body'])
for comment in cursor:
    comment_df = comment_df.append(pd.DataFrame(comment, index=[len(comment_df)]))
print('Load topics: ', len(comment_df))
