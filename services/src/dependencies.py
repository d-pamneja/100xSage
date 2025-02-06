from langchain_community.document_loaders import PyPDFLoader,TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from openai import OpenAI
import requests

from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from pinecone import Pinecone, ServerlessSpec
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_core.prompt_values import PromptValue
from langchain_core.runnables import RunnablePassthrough

from langchain.agents import initialize_agent, Tool
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage

from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import BaseTool
from typing import List

from pydantic import BaseModel, Field
from typing import Optional,List,Type
from pathlib import Path
import yaml

import validators
import requests
import os
import uuid
import boto3

from src.exception import CustomException
from src.logger import logging
from dotenv import load_dotenv
load_dotenv()

import os
import sys
import time
import json

# OpenAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QA_SUMMARISER_OPENAI_ASSISTANT_ID = os.getenv("QA_SUMMARISER_OPENAI_ASSISTANT_ID")

#Pincone API
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_API_ENV = os.getenv("PINECONE_API_ENV")
PINECONE_KNOWLEDGE_BASE_INDEX_NAME = os.getenv("PINECONE_KNOWLEDGE_BASE_INDEX_NAME")
PINECONE_QA_BASE_INDEX_NAME = os.getenv("PINECONE_QA_BASE_INDEX_NAME")

# Pinecone QA Base - ID Creds
ADMIN_ID_QA = os.getenv("ADMIN_ID_QA")
ADMIN_ID_QA_QUERY = os.getenv("ADMIN_ID_QA_QUERY")
COURSE_ID_QA = os.getenv("COURSE_ID_QA")
TOPIC_ID_QA = os.getenv("TOPIC_ID_QA")

# AWS Credentials
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

KNOWLEDGE_BASE_MODIFICATION_QUEUE_URL = os.getenv("KNOWLEDGE_BASE_MODIFICATION_QUEUE_URL")
KNOWLEDGE_BASE_MODIFICATION_NOTIFICATIONS_ARN = os.getenv("KNOWLEDGE_BASE_MODIFICATION_NOTIFICATIONS_ARN")

QA_BASE_MODIFICATION_QUEUE_URL = os.getenv("QA_BASE_MODIFICATION_QUEUE_URL")
QA_BASE_MODIFICATION_NOTIFICATIONS_ARN = os.getenv("QA_BASE_MODIFICATION_NOTIFICATIONS_ARN")
QA_BASE_BUCKET_NAME = os.getenv("QA_BASE_BUCKET_NAME")


