import asyncio
import websockets
import json
from graph_builder import trace_to_graph

PORT = 8765

async def serve(websocket, _):
    with open("graph_data.json") as f:
        graph = json.load(f)
    await websocket.send(json.dumps(graph))

async def main():
    print(f"WebSocket server running at ws://localhost:{PORT}")
    async with websockets.serve(serve, "localhost", PORT):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
