#loading the fastmcp module from mcp
from mcp.server.fastmcp import FastMCP

# Server and routing helper
from starlette.applications import Starlette
import os
from typing import List, Dict

"""
@doc:Starlette:
Starlette is a simple ASGI (ASYNCHRONOUS SERVER GATEWAY INTERFACE) framework for handling concurrent requests
"""
from starlette.routing import Route, Mount
from fastapi import FastAPI
from mcp.server.sse import SseServerTransport
from tavily import TavilyClient
from dotenv import load_dotenv
# Creating SSE bidirectional communication channel over SSE
from starlette.requests import Request 


load_dotenv("./.env")
tavily_api = os.getenv("tavily_api")
mcp = FastMCP(name="Simple mcp server", hostname="127.0.0.1", port=8080)
# Using SSE transporter

tavily_client = TavilyClient(api_key=tavily_api)

## tool to search for web

@mcp.tool("web_search", description="search on web")
def search_web(query, topic="general"):
    if topic not in ["general", "news", "finance"]:
        return None
    response = tavily_client.search(query, topic=topic)
    if response is not None:
        # Format the response to print news title, content, and urls
        if isinstance(response, dict) and "results" in response:
            formatted = []
            for item in response["results"]:
                title = item.get("title", "No Title")
                content = item.get("content", "No Content")
                url = item.get("url", "No URL")
                formatted.append(f"Title: {title}\nContent: {content}\nURL: {url}\n")
            return "\n".join(formatted)
        return formatted
    else:
        return ["Search failed"]  # Return error message


def __helper(crawl_resp):
    if crawl_resp is not None:
        if isinstance(crawl_resp, Dict) and "results" in crawl_resp:
            formatted_results = []
            for dict in crawl_resp["results"]:
                title = dict.get("title", "No Title")
                raw_content = dict.get("raw_content", "No Content")
                url = dict.get("url", "No URL")
                favicon = dict.get("favicon", "")
                formatted_results.append(
                    {
                        "title": title,
                        "raw_content": raw_content,
                        "url": url,
                        "favicon": favicon,
                    }
                )
            return formatted_results

    else:
        return []


# Crawling tool - Tavily
@mcp.tool("web_crawl", description="crawl the web through url and extract the content.")
def web_crawler(url: str, *, instruction="") -> List[Dict]:
    """
    Tavily web-crawler API. Helps to crawl a web page through a particular URL.
    Response structure:
    {
        "base_url": "docs.tavily.com",
        "results": [
            {
                "url": "...",
                "raw_content": "...",
                "favicon": "..."
            },
        ],
        "response_time": 1.23
    }
    With instruction parameter specified, it provides clearer context to crawler on what to crawl.
    """
    crawl_resp = None
    response = []
    if instruction != "":
        crawl_resp = tavily_client.crawl(
            url, instructions=instruction, format="markdown"
        )

    else:
        crawl_resp = tavily_client.crawl(url, format="markdown")

    response = __helper(crawl_resp)

    return response if response is not None else []


transport = SseServerTransport("/message")  # Accepts messages from client side


async def handle_sse(request: Request):
    try:
        async with transport.connect_sse(
            request.scope, request.receive, request._send
        ) as (in_stream, out_stream):
            # Wait for message from client-side (e.g., POST message or RPC)
            await mcp._mcp_server.run(
                in_stream, out_stream, mcp._mcp_server.create_initialization_options()
            )
    except Exception as e:
        print("Server handler error:", e)


sse_app = Starlette(
    # Client achieves persistent connection to server for sending streams of events like GET, POST Message passing b/w client and server
    routes=[
        Route(
            "/sse", handle_sse, methods=["GET"]
        ),  # Server sending GET request to client
        Mount(
            "/message/", app=transport.handle_post_message
        ),  # Client response message is redirected to server
    ]
)

# Creating a FastAPI-based communication interface
app = FastAPI()
app.mount("/", sse_app)
if __name__ == "__main__":
    print("Starting the server....")
    import uvicorn  # Enable both HTTP and SSE

    uvicorn.run(app, host="127.0.0.1", port=8080)
