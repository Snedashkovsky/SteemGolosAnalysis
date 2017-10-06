#!/usr/bin/python3
from pymongo import MongoClient
import pandas as pd

def to_xml(df, filename=None, mode='w'):
    def row_to_xml(row):
        xml = ['<item>']
        for i, col_name in enumerate(row.index):
            xml.append('  <field name="{0}">{1}</field>'.format(col_name, row.iloc[i]))
        xml.append('</item>')
        return '\n'.join(xml)
    res = '\n'.join(df.apply(row_to_xml, axis=1))

    if filename is None:
        return res
    with open(filename, mode) as f:
        f.write(res)

pd.DataFrame.to_xml = to_xml



mongo = MongoClient(host=['localhost:27017'])
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

comment_df.to_xml('foo.xml')
