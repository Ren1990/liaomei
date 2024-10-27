import google.generativeai as genai
import os
import textwrap
import pandas as pd
import numpy as np
import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

#agent functions
def menu():
    bar1, bar2= st.columns([1,1])
    bar1.page_link("meizixiangshenme.py", label="了如指掌", icon="👧")
    bar2.page_link("pages/junshiliangji.py", label="坐筹帷幄", icon="💡")
    st.write("")

def make_prompt(prompt, meizi_message):
  #escaped = passage.replace("'", "").replace('"', "").replace("\n", " ")
  prompt = textwrap.dedent("""
你是一个恋爱专家，你专门帮助男生理解他们喜欢的女生寄给他们的讯息，解读女生讯息背后的含义和她们的心情与想法。
男生将会向你请求写讯息给女生的建议，尤其是希望你能给出例子，以打动对方的心。
男生请求: {prompt}
以下开始是女生和男生的电话讯息：{meizi_message}
""").format(prompt=prompt, meizi_message=meizi_message)
  return prompt

def make_prompt2(prompt):
  #escaped = passage.replace("'", "").replace('"', "").replace("\n", " ")
  prompt = textwrap.dedent("""
你是一个恋爱专家。
以下是男生请求: {prompt}                          
""").format(prompt=prompt)
  return prompt

def gemini_chat(full_prompt):
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    answer = model.generate_content(full_prompt)
    for chunk in answer.text:
        yield chunk   

def update_knowledge():
    docdir='rag_docs/'
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    table=pd.DataFrame(columns=['document', 'content','embedding','relevant score'])
    i=0
    for doc in os.listdir(docdir):
        docsplit=TextLoader(docdir+doc,encoding='utf8').load_and_split(text_splitter)
        for chunk in docsplit:
            embedding = genai.embed_content(model='models/text-embedding-004',content=chunk.page_content,task_type="retrieval_query")
            table.loc[i]=[chunk.metadata['source'],chunk.page_content,embedding['embedding'],0]
            i=i+1
    return table

def retrieve_knowledge(query):
  rank_threshold=0.5
  ranking=10
  readparquet=pd.read_parquet('embbed_table.parquet.gzip')
  query_embedding = genai.embed_content(model='models/text-embedding-004',
                                        content=query,
                                        task_type="retrieval_query")
  readparquet['relevant score'] = np.dot(np.stack(readparquet['embedding']), query_embedding["embedding"])
  relevant_knowledge=readparquet.loc[(readparquet['relevant score']>rank_threshold)].sort_values('relevant score',ascending=False).head(ranking)
  text_list=[]
  i=1
  for t in relevant_knowledge['content'].apply(lambda x: x.replace("\ufeff", "")):
    text_list.append("KNOWLEDGE "+str(i)+": "+t+" ")
    i=i+1

  return "".join(text_list)