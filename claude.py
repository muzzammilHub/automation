from anthropic import AnthropicBedrock
from langfuse import Langfuse
import uuid
import json
import os
from dotenv import load_dotenv

load_dotenv()

anthropic = AnthropicBedrock(
  aws_secret_key = os.getenv("aws_secret_key"),
  aws_access_key = os.getenv("aws_access_key"),
  aws_region = 'us-east-1',
)

langfuse = Langfuse(
  secret_key = os.getenv("secret_key"),
  public_key = os.getenv("public_key"),
  host = "https://cloud.langfuse.com",
)

session_id = str(uuid.uuid4())

def callLLMHaikuViaMessages(system, messages, user, temperature=0, model="claude-3-haiku-20240307", meta={}):
    trace = langfuse.trace(
        name=user,
        session_id=session_id,
        input=json.dumps(messages),
        user_id=meta.get("type", "no-type"),
        version=model
    )

    max_tokens = 2048

    generation = trace.generation(
        name="chat-completion",
        model=model,
        model_parameters={
            "temperature": temperature,
            "max_tokens": max_tokens
        },
        input=[{"role": "system", "content": system}] + messages
    )

    result = anthropic.messages.create(
        temperature= temperature,
        system= system,
        messages = messages,
        model= model,
        max_tokens= max_tokens,
    )

    metadata = {}

    trace.update(
        output=result,
        metadata = metadata,
    )

    generation.end(
        output= result,
        version= model
    )

    return result.content[0].text


