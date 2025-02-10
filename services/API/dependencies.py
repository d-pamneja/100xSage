from fastapi import FastAPI, Depends, HTTPException, status, Query,Body, APIRouter,BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field, ValidationError
from typing import List, Union, Dict, Optional,Literal,Any
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
import validators
from requests import request
import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
import redis
import threading
import boto3
import asyncio
import json
import sys
import time
import websockets
import random

import os
from dotenv import load_dotenv
load_dotenv()

DISCORD_AUTH_TOKEN = os.getenv('DISCORD_AUTH_TOKEN')
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_GATEWAY_URL = os.getenv('DISCORD_GATEWAY_URL')
DISCORD_GUILD_ID = os.getenv('DISCORD_GUILD_ID')
DISCORD_PARENT_ID = os.getenv('DISCORD_PARENT_ID')

