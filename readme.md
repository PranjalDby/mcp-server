🧠 MCP Server with Tavily Web Search Integration

mcp-server is a lightweight Model Context Protocol (MCP) server that integrates the Tavily Search API to enable real-time internet access for Large Language Models (LLMs). It allows LLMs to fetch up-to-date, factual information from the web instead of relying solely on static training data.

This server acts as a bridge between LLMs and live web data, making it ideal for applications that require current news, recent documentation, live trends, or fast-changing technical information.

✨ Key Features

🔗 MCP-compliant server for seamless LLM integration

🌐 Real-time web search powered by the Tavily API

🤖 Designed specifically for LLMs needing fresh, current information

⚡ Simple, minimal Python implementation

🧩 Easy to extend with additional tools or data sources

🛠 Use Cases

LLM agents with live internet search

AI assistants requiring recent or time-sensitive data

Research and Q&A systems beyond training-cutoff limits

Developer tools that need real-world, current context

📦 Tech Stack

Python

Model Context Protocol (MCP)

Tavily Search API

## Prerequisites

- Node.js (v16 or higher recommended)
- npm or yarn
- (Optional) Docker

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/mcp_demo.git
cd mcp_demo
npm install
# or
yarn install
```

## Configuration

- Create `.env` file and create the variable named `tavily_api` and put your tavily api key. e.g = "tavily_api = apikey"

## Running the Server

### Development

```bash
npm run dev
# or
yarn dev
```

### Production

```bash
npm run build
npm start
# or
yarn build
yarn start
```
### Python
```
install python if not present
run following commands:
cd mcp_demo folder
python -r requirement.txt
python server.py

```
python server.py

### Using Docker (Optional)

```bash
docker build -t mcp_demo .
docker run -p 3000:3000 mcp_demo
```

## API Usage

The server exposes RESTful APIs. By default, it runs on `http://localhost:8080`.

Refer to the source code or API documentation for more details.

## Project Structure

```
mcp_demo/
├── .env (may not be present. please create .env file)
├── requirement.txt
├── server.py
└── ...
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/feature-name`)
3. Commit your changes
4. Push to the branch (`git push origin feature/feature-name`)
5. Open a pull request

## License

This project is licensed under the MIT License.
