""" Configuration for the Anthropic model and loading environment variables."""

from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv, find_dotenv
import os

# FINDING ENV FILE AND LOADING ENV VARIABLES
find_dotenv(load_dotenv())

model = ChatAnthropic(model="claude-haiku-4-5-20251001", api_key=os.getenv("ANTHROPIC_API_KEY"))