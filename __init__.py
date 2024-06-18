# Importations de bibliothèques
from bs4 import BeautifulSoup
import requests
import urllib.request, urllib.parse, urllib.error
import ssl
import json
import calendar
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy 
import time
import os
import warnings
from langdetect import detect
import uuid
import random as rd 
warnings.filterwarnings("ignore", category=UserWarning)
from torpy.http.requests import TorRequests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)