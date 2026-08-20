import os
from google import genai
from google.genai import types, errors
from tools import AVAILABLE_TOOLS
from schema import RestaurantRecommendations


class RestaurantAgent:
    def __init__(self):
        self.client = genai.Client()
        self.model_name = "gemini-3.1-flash-lite"
        
        system_instruction = (
            "You are a local culinary concierge agent. Your goal is to recommend the best "
            "restaurants based strictly on area and food type parameters. Always prioritize "
            "using your local search tools over your internal pre-trained memory. "
            "When presenting options, summarize the pricing, specific specialty, and location."
        )
        
        self.config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=list(AVAILABLE_TOOLS.values()),
            temperature=0.1,  # Low temperature guarantees deterministic tool usage
            # response_mime_type="application/json",
            # response_schema=RestaurantRecommendations,
        )
        self.chat = self.client.chats.create(model=self.model_name, config=self.config)


    def ask(self, user_query: str):
        try:
            print(f"\n[User Query]: {user_query}")
            response = self.chat.send_message(user_query)
            
            while response.function_calls:
                for call in response.function_calls:
                    tool_name = call.name
                    tool_args = call.args
                    
                    print(f"🔍 [Agent Action]: Invoking local tool '{tool_name}' with arguments: {tool_args}")
                    
                    if tool_name in AVAILABLE_TOOLS:
                        tool_output = AVAILABLE_TOOLS[tool_name](**tool_args)
                    else:
                        tool_output = {"error": f"Tool '{tool_name}' is unavailable."}
                    
                    # Push tool findings back into Gemini's context window
                    response = self.chat.send_message(
                        types.Part.from_function_response(
                            name=tool_name,
                            response={"result": tool_output}
                        )
                    )
            
            print(f"🤖 [Agent Recommendation]:\n{response.text}")
            return response.text
        except errors.ClientError as e:
            # 400 Bad Request, 403 Forbidden, 429 Rate Limit
            print(f"Client Error Occurred: {e}")
        except errors.ServerError as e:
            print(f"Server Error Occurred: {e}")
