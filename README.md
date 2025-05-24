# YouTube Summary API

A FastAPI service that analyzes and summarizes YouTube video transcripts using OpenAI via n8n.

## Features

- YouTube video transcript analysis
- OpenAI integration via n8n
- RESTful API with FastAPI
- Data validation with Pydantic

## Prerequisites

- Python 3.8+
- Docker (optional)
- A configured n8n instance with an OpenAI webhook

## Installation

1. Clone the repository:
```bash
git clone [REPO_URL]
cd youtube-summary-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
export N8N_AI_WEBHOOK="your_n8n_webhook_url"
```

## Usage

1. Start the API:
```bash
uvicorn main:app --reload
```

2. The API will be available at: `http://localhost:8000`

### Endpoints

#### POST /analyze
Analyzes a YouTube video transcript.

**Request body:**
```json
{
    "video_id": "VIDEO_ID",
    "transcript": "VIDEO_TRANSCRIPT"
}
```

## Docker Deployment

1. Build the image:
```bash
docker build -t youtube-summary-api .
```

2. Run the container:
```bash
docker run -p 8000:8000 -e N8N_AI_WEBHOOK="your_n8n_webhook_url" youtube-summary-api
```

## Project Structure

```
youtube-summary-api/
├── app/
│   └── routes.py
├── main.py
├── requirements.txt
├── Dockerfile
└── README.md
```

## License

MIT License

Copyright (c) 2025 YouTube Summary API

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.
