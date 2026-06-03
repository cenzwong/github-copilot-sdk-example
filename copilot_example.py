import asyncio

from copilot import CopilotClient
from copilot.session_events import AssistantMessageData, SessionIdleData
from copilot.session import PermissionHandler

async def main():
    client = CopilotClient()
    await client.start()

    # Create a session (on_permission_request is optional; approve_all allows every tool)
    session = await client.create_session(
        on_permission_request=PermissionHandler.approve_all,
        model="gpt-5-mini",
    )

    done = asyncio.Event()

    def on_event(event):
        match event.data:
            case AssistantMessageData() as data:
                print(data.content)
            case SessionIdleData():
                done.set()

    session.on(on_event)
    await session.send("What is 2+2?")
    await done.wait()

    # Clean up manually
    await session.disconnect()
    await client.stop()

asyncio.run(main())