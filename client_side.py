import asyncio
import traceback
from mcp import ClientSession,StdioServerParameters
from mcp.client.sse import sse_client
from contextlib import AsyncExitStack
from typing import Optional
from dotenv import load_dotenv
from anthropic import Anthropic
# async def connect_server():
#     sse_url = "http://localhost:8080/sse/"  # Changed from 8050 to 8080
#     try:
#         print("Connecting to SSE server...")
#         # open sse => instream and outstream
#         async with sse_client(url=sse_url) as (in_stream, out_stream):
#             print("SSE connection established.")
#             # creating our mcp session over this streams
#             async with ClientSession(in_stream, out_stream) as session:
#                 print("MCP session started.")
#                 # initialize
#                 info = await session.initialize()
#                 print(f"server info:\nconnected to: {str(info.serverInfo)}")
#                 # listing the available tools
#                 tools = await session.list_tools()
#                 print("Available tools: ", tools)
#                 print("Calling tool 'web_search'...")
#                 print("What u want:::::\n")
#                 wanting = input()
#                 result = await session.call_tool(name='web_search', arguments={'query': f'{wanting}', 'topic': 'general'})
#                 print("Tool call completed. Result received:")
#                 print("--------------------------------------------xxxxxxxxxxxx-------------------------------------------------")
#                 print(result.content[0].text)
#     except Exception as e:
#         print("Exception occurred:", e)
#         traceback.print_exc()

class MCPClient:
    def __init__(self):
        self.session:Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic


    # methods...
    async def connect_to_server(self,server_script_path:str):
        """
        MCP server: this method connects u to ur mcp server

        @args: server path (.py)
        """
        sse_url = "http://localhost:8080/sse/"  # currently a localhost url is given
        try:
            print("Connecting to SSE server...")
            # open sse => instream and outstream
            async with sse_client(url=sse_url) as (in_stream, out_stream):
                print("SSE connection established.")
                # creating our mcp session over this streams
                async with ClientSession(in_stream, out_stream) as self.session:
                    print("MCP session started.")
                    # initialize
                    info = await self.session.initialize()
                    print(f"server info:\nconnected to: {str(info.serverInfo)}")
                    # listing the available tools
                    tools = await self.session.list_tools()
                    tools_list = tools.tools
                    print("Available tools: ",[tool.name for tool in tools_list])
                    # print("Calling tool 'web_search'...")
                    # print("What u want:::::\n")
                    # wanting = input()
                    # result = await session.call_tool(name='web_search', arguments={'query': f'{wanting}', 'topic': 'general'})
                    # print("Tool call completed. Result received:")
                    # print("--------------------------------------------xxxxxxxxxxxx-------------------------------------------------")
                    # print(result.content[0].text)
        except Exception as e:
            print("Exception occurred:", e)
            traceback.print_exc()

    async def process_query(self,query:str)->str:
        """process query using Claude and available tools"""
        message = [
            {
                "role":"user",
                "content":query
            }
        ]
        response = await self.session.list_tools()
        tools_list = response.tools
        available_tools = [{
            "name": tool.name,
            "description": tool.description
        } for tool in tools_list]
        # ...use available_tools as needed...


    ### working just fine
if __name__ == "__main__":
    try:
        asyncio.run() # running the client_side
    except Exception as e:
        print("Closed....")