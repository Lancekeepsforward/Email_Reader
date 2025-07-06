# Email Reader - AI-Powered Email Assistant

An intelligent email management system that uses RAG (Retrieval-Augmented Generation) and AI agents to help you search, analyze, and interact with your emails through natural language conversations.

## 🚀 Features

- **Gmail Integration**: Fetch and parse emails from Gmail using the Gmail API
- **AI-Powered Search**: Use natural language to search through your emails
- **RAG Architecture**: Retrieval-Augmented Generation for context-aware responses
- **Vector Search**: FAISS-based semantic search for finding relevant emails
- **Conversational AI**: Chat with an AI agent about your emails
- **Web Search Integration**: Combine email data with web search results
- **Multi-Model Support**: Compatible with Groq, Llama, and other LLM providers

## 🏗️ Architecture

The project follows a modular architecture with the following components:

```
Email_Reader/
├── src/email_agent/
│   ├── agent/           # AI agent implementations
│   ├── config/          # Configuration and embedding models
│   ├── utils/           # Email fetching, parsing, and utilities
│   └── web/             # Web search functionality
├── scripts/             # Utility scripts
├── docs/                # Documentation
└── test/                # Test files
```

### Core Components

- **BaseAgent**: Main AI agent with RAG capabilities
- **EmailFetcher**: Gmail API integration for fetching emails
- **EmailParser**: Parse and structure email content
- **VectorStore**: FAISS-based semantic search index
- **WebSearch**: Google Custom Search integration

## 📋 Prerequisites

- Python 3.8+
- Gmail account with API access
- Groq API key (or other LLM provider)
- Google Custom Search API (optional, for web search)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Email_Reader
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   # Gmail API Configuration
   CONFIG_DIR=./src/email_agent/config
   
   # LLM Configuration
   GROQ_API_KEY=your_groq_api_key
   LLAMA3_8B=llama3-8b-8192
   MODEL_DEEPSEEK1=deepseek-chat
   
   # Embedding Model
   EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
   
   # Web Search (Optional)
   GOOGLE_API_KEY=your_google_api_key
   SEARCH_ENGINE_ID=your_search_engine_id
   WEB_DIR=./src/email_agent/web
   ```

4. **Set up Gmail API credentials**
   - Download your `client_secret.json` from Google Cloud Console
   - Place it in the project root
   - Run the credential setup (first run will authenticate you)

## 🚀 Usage

### 1. Fetch Emails

```bash
python -m src.email_agent.utils.email_fetcher
```

This will prompt you for:
- Number of emails to fetch
- Search query (default: Columbia emails)

### 2. Parse Emails

```bash
python -m src.email_agent.utils.email_parser
```

This processes the fetched emails and creates structured data.

### 3. Start the AI Assistant

```bash
python -m src.email_agent.main
```

This launches the interactive chat interface where you can:
- Ask questions about your emails
- Search for specific content
- Get AI-powered insights

### 4. Web Search Integration

```bash
python -m src.email_agent.web.search
```

Combine email data with web search results for comprehensive answers.

## 💬 Example Conversations

```
You: Find emails about project deadlines
Agent: I found 3 emails related to project deadlines. Here are the key details...

You: What was the last communication from John?
Agent: The most recent email from John was about...

You: Summarize all emails from this week
Agent: Here's a summary of this week's emails...
```

## 🔧 Configuration

### Agent Rules

Configure agent behavior in `config/rules_agents.json`:
```json
[
  {
    "role": "system",
    "content": "You are a helpful email assistant..."
  }
]
```

### Embedding Models

The system supports multiple embedding models:
- `all-MiniLM-L6-v2` (default)
- `Qwen3-Embedding-0.6B`
- Custom models

### Vector Store

Emails are indexed using FAISS for fast semantic search. The index is automatically updated when new emails are added.

## 📊 Data Flow

1. **Email Fetching**: Gmail API → Email IDs and metadata
2. **Email Parsing**: Raw emails → Structured EmailSample objects
3. **Vector Indexing**: Email content → FAISS vector store
4. **Query Processing**: User input → Semantic search → RAG response
5. **AI Response**: Context + Query → LLM → Natural language response

## 🔒 Security

- API keys are stored in environment variables
- Gmail credentials are handled securely through OAuth2
- No sensitive data is logged or stored in plain text

## 🧪 Testing

Run tests to verify functionality:
```bash
python -m pytest test/
```

## 📝 Dependencies

### Core Dependencies
- `langchain-community>=0.3.1` - LangChain community components
- `langchain-groq>=0.3.1` - Groq LLM integration
- `langchain-huggingface>=0.3.1` - HuggingFace embeddings
- `groq>=0.1.1` - Groq API client

### Gmail Integration
- `google-api-python-client==2.174.0` - Gmail API client
- `google-auth==2.40.3` - Google authentication

### Utilities
- `dotenv>=1.0.1` - Environment variable management
- `jsonpath-ng>=1.6.0` - JSON path processing
- `requests>=2.18.0` - HTTP requests

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **Gmail API Quota Exceeded**
   - Check your Gmail API quota in Google Cloud Console
   - Reduce the number of emails fetched

2. **Embedding Model Not Found**
   - Ensure the model name is correct
   - Check if the model is available in your environment

3. **Vector Store Errors**
   - Delete the existing FAISS index to rebuild
   - Check file permissions in the config directory

### Getting Help

- Check the logs for detailed error messages
- Verify all environment variables are set correctly
- Ensure all dependencies are installed

## 🔮 Future Enhancements

- [ ] Multi-agent collaboration
- [ ] Task delegation capabilities
- [ ] Enhanced contextual reasoning
- [ ] Email summarization
- [ ] Sentiment analysis
- [ ] Email categorization
- [ ] Integration with other email providers
