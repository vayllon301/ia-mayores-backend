# IA Mayores Backend

A conversational AI chatbot API designed for seniors, featuring natural weather integration powered by LangChain and OpenAI.

## Features

- 🤖 Conversational AI chatbot using GPT-4
- 🌤️ Real-time weather information integration
- 💬 Conversation memory for contextual responses
- 🚀 Production-ready FastAPI backend
- ☁️ Azure Web App ready

## Tech Stack

- **Framework**: FastAPI
- **AI/ML**: LangChain, OpenAI GPT
- **Weather API**: Open-Meteo (free, no API key required)
- **Server**: Uvicorn/Gunicorn
- **Python**: 3.11+

## Local Development

### Prerequisites

- Python 3.11 or higher
- OpenAI API key

### Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd IA-Mayores-Backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

5. Run the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Testing

Run the test script:
```bash
python test_chatbot.py
```

## API Endpoints

### `GET /`
Health check endpoint
```json
{
  "status": "healthy",
  "message": "IA Mayores Backend is running",
  "version": "1.0.0"
}
```

### `GET /health`
Azure health check endpoint

### `POST /chat`
Main chat endpoint

**Request:**
```json
{
  "message": "What's the weather like in Madrid?"
}
```

**Response:**
```json
{
  "response": "Right now in Madrid, Spain, it's 15°C with clear sky. Perfect weather for a walk! The humidity is at 60% and there's a gentle breeze at 10 km/h."
}
```

## Deployment

### Azure Web App

For detailed Azure deployment instructions, see [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md)

**Quick Start:**
1. Create an Azure Web App with Python 3.11
2. Set `OPENAI_API_KEY` in Application Settings
3. Set startup command from `startup.txt`
4. Deploy via GitHub Actions, Local Git, or ZIP

**Startup Command:**
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000 --timeout 120
```

## Project Structure

```
IA-Mayores-Backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── chain.py         # LangChain agent configuration
│   ├── weather.py       # Weather tool implementation
│   └── memory.py        # (Future) Memory management
├── requirements.txt      # Python dependencies
├── startup.txt          # Azure startup command
├── .env                 # Environment variables (local only)
├── .gitignore          # Git ignore rules
├── test_chatbot.py     # Test script
└── README.md           # This file
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT models | Yes |

## Features in Detail

### Weather Integration
- Uses Open-Meteo free API (no key required)
- Provides current weather data for any location
- Natural language integration in responses
- Includes temperature, conditions, humidity, and wind speed

### Conversational Memory
- Maintains conversation context
- Remembers previous exchanges within a session
- Enables follow-up questions

### Natural Language Processing
- Powered by LangChain agents
- Tool-augmented generation
- Context-aware responses

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[Your License Here]

## Support

For issues or questions, please open an issue on GitHub.
