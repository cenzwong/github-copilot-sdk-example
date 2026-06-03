
import asyncio
from copilot import CopilotClient
from copilot.session import PermissionHandler


def format_model_cost(model) -> str:
    billing = getattr(model, "billing", None)
    if billing is None:
        return "Not exposed by SDK"

    multiplier = getattr(billing, "multiplier", None)
    if multiplier is None:
        return "Not exposed by SDK"

    return f"{multiplier}x base rate"


async def main():
    client = CopilotClient()
    await client.start()

    # Retrieve available models
    models = await client.list_models()
    
    print("Available Copilot Models:")
    for model in models:
        # SDK model metadata uses `name`; vendor is not always exposed.
        print(f"- ID: {model.id}")
        print(f"  Name: {getattr(model, 'name', 'Unknown')}")
        max_ctx = getattr(model.capabilities.limits,
                          "max_context_window_tokens", None)
        print(f"  Max Context Tokens: {max_ctx}")
        supports_vision = getattr(model.capabilities.supports,
                                  "vision", False)
        print(f"  Supports Vision: {supports_vision}")
        print(f"  Cost: {format_model_cost(model)}")
        print("-" * 40)

    # Example: Dynamic validation before session creation
    target_model = "gpt-5-mini"
    available_ids = [m.id for m in models]
    
    if target_model in available_ids:
        await client.create_session(
            on_permission_request=PermissionHandler.approve_all,
            model=target_model,
        )
    else:
        print(f"Warning: {target_model} not available. Defaulting to fallback.")

asyncio.run(main())