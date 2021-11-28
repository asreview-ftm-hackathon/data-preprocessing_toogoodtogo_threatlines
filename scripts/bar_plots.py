# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 20:06:35 2021

@author: dinterr
"""

"""Main script to preprocess FTM data."""
import load_data
import pandas as pd

df = load_data.get_data(r'../data/processed_data.csv')

df['email_sender'] = df['email_sender'].apply(lambda x: x if len(str(x)) < 60 else None)

ax = df['email_sender'].value_counts()[df['email_sender'].value_counts()> 10].plot.bar()

fig = ax.get_figure()
fig.savefig('../figures/bar_email_sender.png')
#%%
df['email_receiver'] = df['email_receiver'].apply(lambda x: x if len(str(x)) < 60 else None)

ax = df['email_receiver'].value_counts()[df['email_receiver'].value_counts()> 10].plot.bar()

fig = ax.get_figure()
fig.savefig('../figures/bar_email_receiver.png')
#%%
ax = df.doc_type.value_counts().plot.bar()
fig = ax.get_figure()
fig.savefig('../figures/bar_doc_type.png')
#%%
df["date"] = pd.to_datetime(df.date)

ax = df.groupby([df["date"].dt.year, df["date"].dt.month]).index.count().plot.bar(figsize=(40,8))
fig = ax.get_figure()
fig.savefig('../figures/bar_date.png')
#%%
df["betterDate"] = pd.to_datetime(df.betterDate, utc=True)
ax = df.groupby([df["betterDate"].dt.year, df["betterDate"].dt.month]).index.count().plot.bar(figsize=(40,8))
fig = ax.get_figure()
fig.savefig('../figures/bar_betterDate.png')
