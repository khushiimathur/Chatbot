# Chatbot
# Telegram Bot with Gemini AI Integration

## Overview

This Telegram bot leverages the Telethon library and Gemini AI to provide various functionalities, including user registration, contact sharing, file analysis, and web search. The bot is built using Python and integrates with MongoDB for data storage.

## Features

- **User Registration**: Saves user's first name, username, and chat ID upon the first interaction.
- **Contact Sharing**: Requests and stores the user's phone number.
- **File Analysis**: Accepts image files and provides a description of the content using Gemini AI. Stores file metadata in MongoDB.
- **Web Search**: Allows users to perform a web search using the Google Custom Search API and returns an AI summary of the search results with top web links.

## Prerequisites

- Python 3.6+
- Telegram account
- MongoDB instance (local or cloud)
- Google Custom Search API key and Search Engine ID
- Gemini AI API key


## Commands
/start: Initiates the bot and registers the user.

/query: Prompts the user to enter a query for Gemini AI.

/websearch: Prompts the user to enter a search query for web search.
