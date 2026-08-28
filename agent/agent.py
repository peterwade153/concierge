import os
import re
import json
from typing import Optional

from openai import OpenAI

from agent.tools import AVAILABLE_TOOLS, TOOL_SCHEMAS
from agent.schema import RestaurantRecommendations


class RestaurantAgent:
    def __init__(self):

        if not os.environ.get("OPENROUTER_API_KEY"):
            raise ValueError("OPENROUTER_API_KEY environment variable is not set.")

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ.get("OPENROUTER_API_KEY"),
        )
        self.model_name = "meta-llama/llama-4-scout"

        self.system_instruction = (
            "You are a local culinary concierge agent. Your goal is to recommend the best "
            "restaurants based strictly on area and food type parameters. Always prioritize "
            "using your local search tools over your internal pre-trained memory. \n\n"
            "CRITICAL: You MUST respond strictly in raw JSON adhering to this schema:\n"
            "1. You MUST output ONLY raw, valid JSON. No conversational text.\n"
            "2. Do NOT wrap your output in markdown blocks (DO NOT use ```json or ```).\n"
            "3. Your response MUST begin with the opening brace '{' and end with the closing brace '}'.\n"
            "4. Adhere strictly to this JSON Schema:\n"
            f"{json.dumps(RestaurantRecommendations.model_json_schema())}"
        )

        self.tools = list(TOOL_SCHEMAS.values())

        self.messages = [{"role": "system", "content": self.system_instruction}]
        return

    def _extract_and_parse_json(self, raw_text: str) -> Optional[RestaurantRecommendations]:
        """Sanitizes LLM response text from markdown or stray wrappers and parses into Pydantic model."""
        if not raw_text:
            return None

        text = re.sub(r"^```[a-zA-Z]*\s*|\s*```$", "", raw_text.strip(), flags=re.DOTALL)

        if not text.startswith("{"):
            if not text.startswith('"'):
                text = '"' + text
            text = "{" + text
        if not text.endswith("}"):
            text = text + "}"

        try:
            data = json.loads(text)
            return RestaurantRecommendations.model_validate(data)
        except Exception as e:
            print(f"❌ [Parsing Error]: Could not validate model payload: {e}")
            print(f"Raw response text was:\n{raw_text}")
            return None

    def ask(self, user_query: str) -> Optional[RestaurantRecommendations]:
        try:
            print(f"\n[User Query]: {user_query}")
            self.messages.append({"role": "user", "content": user_query})

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=self.messages,
                tools=self.tools,
                temperature=0.1,
                response_format={"type": "json_object"},
            )

            response_message = response.choices[0].message

            # Process tool calls in a loop until the model returns a final text response
            while response_message.tool_calls:
                # Add the assistant's request (with tool calls) to history
                self.messages.append({
                    "role": "assistant",
                    "content": response_message.content or "",
                    "tool_calls": response_message.tool_calls,
                })

                for tool_call in response_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments or "{}")


                    if tool_name in AVAILABLE_TOOLS:
                        tool_output = AVAILABLE_TOOLS[tool_name](**tool_args)
                    else:
                        tool_output = {"error": f"Tool '{tool_name}' is unavailable."}

                    self.messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(tool_output),
                        }
                    )

                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=self.messages,
                    tools=self.tools,
                    temperature=0.1,
                    response_format={"type": "json_object"},
                )
                response_message = response.choices[0].message

            final_text = response_message.content
            result = self._extract_and_parse_json(final_text)
            if result is None:
                return

            self.messages.append({"role": "assistant", "content": final_text})
            print(f"🤖 [Agent Recommendation]:\n{result.model_dump_json(indent=2)}")
            return result

        except Exception as e:
            print(f"Error occurred during API request: {e}")
        return None
