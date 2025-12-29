from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools import tool

load_dotenv()

@tool("get_current_datetime")
def get_current_datetime():
    """Returns the current date and time as a string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

model = ChatOpenAI(model_name="gpt-4o")

model_with_tools = model.bind_tools([get_current_datetime])

response = model_with_tools.invoke("What is the current date? Just mention the date")

# print(response)

# python ./Tool-calling/custom_tools/datetime_tool.py
# content='' 
# additional_kwargs={'refusal': None} 
# response_metadata={'token_usage': {'completion_tokens': 11, 'prompt_tokens': 52, 'total_tokens': 63, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0
#             }, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0
#             }
#         }, 'model_provider': 'openai', 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_cbf1785567', 'id': 'chatcmpl-Cs1dXUwELZEl8dMK0H7420QZ6dvo1', 'service_tier': 'default', 'finish_reason': 'tool_calls', 'logprobs': None
#     } id='lc_run--019b68ee-c5b7-79a2-9f38-2ac5117244fe-0' 
# tool_calls=[
#         {'name': 'get_current_datetime', 'args': {}, 'id': 'call_xCJpLiXxRNrukOTAxFPB9MFF', 'type': 'tool_call'
#         }
#     ] usage_metadata={'input_tokens': 52, 'output_tokens': 11, 'total_tokens': 63, 'input_token_details': {'audio': 0, 'cache_read': 0
#         }, 'output_token_details': {'audio': 0, 'reasoning': 0
#         }
#     }

# There is no content, because LLM can not answer this qiery directly, It need to help from tools.
# It mentioned the tools to call to answer this query, LLM won't call tools, they just decide. 
# The system (Host) needs to call that tool and comunicate back to LLM with tool message.

print(response.tool_calls)
# [{'name': 'get_current_datetime', 'args': {}, 'id': 'call_x5hIYqOJp57NvU6AGP9baQgH', 'type': 'tool_call'}]