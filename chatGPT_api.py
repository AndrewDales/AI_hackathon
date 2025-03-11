from openai import OpenAI
from typing_extensions import override
import json

client = OpenAI(
    api_key="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")
gptModel = "gpt-4-turbo"


def get_GPT_response(prompt, systemRole="You are a helpful assistant.", reponseFormat='text', json_schema=None):
    """
    Function to send a text prompt (and optionally an image) to OpenAI's GPT model.


    Parameters:
    - prompt (str): The user input or question.
    - systemRole (str): System instructions for GPT behavior.
    - responseFormat (str): "text" or "json_object" or "json_schema".
    - json_schema (dict): JSON schema if using responseFormat="json_schema".
    - gptModel (str): Model name (e.g., "gpt-4o").
    - image_url (str): URL of an image (optional).


    Returns:
    - response (str/dict): The model's response.
    """

    if reponseFormat != "json_schema":
        completion = client.chat.completions.create(
            model=gptModel,
            messages=[
                {"role": "system", "content": systemRole},
                {
                    # instructions that request an output
                    "role": "user",
                    "content": prompt
                }],
            response_format={"type": reponseFormat}
        )

        response = completion.choices[0].message.content


    else:
        completion = client.chat.completions.create(
            model=gptModel,
            messages=[
                {"role": "system", "content": systemRole},
                {
                    # instructions that request an output
                    "role": "user",
                    "content": prompt
                }],
            response_format={"type": "json_object"},
            tool_choice="auto",
            tools=[{"type": "function", "function": {"name": "get", "parameters": json_schema}}]
        )

        response = completion.choices[0].message.tool_calls[0].function.arguments

    print(response)
    tokens_used = completion.usage.total_tokens

    # Pricing per 1,000 tokens (as of 2024, update with OpenAI’s pricing)
    PRICING = {
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},  # Prices in dollars per 1k tokens
    }
    model_pricing = PRICING.get(gptModel, {"input": 0.15 / 1000, "output": 0.6 / 1000})
    cost = (tokens_used / 1000) * model_pricing["input"]

    print(f"Tokens used: {tokens_used}, Estimated cost: ${cost:.6f}")

    return (response)


if __name__ == "__main__":
    print("****FIRST PROMPT****")
    prompt = "give me five interesting facts about Shakespeare"
    systemRole = "you are a bot making quiz questions for age 12-18 and provide your output in json format"
    data = get_GPT_response(prompt, systemRole, reponseFormat="json_object")

    try:
        jData = json.loads(data)
    except:
        print("invalid json format")

    print("****SECOND PROMPT****")
    prompt = "give me 10 jokes, each with a comedy score out of 10. Give it in a JSON format, for example - joke: text, score: score. Do not give me anything other than the JSON response"
    systemRole = "you are a joke creating bot"
    data = get_GPT_response(prompt, systemRole)

    print("****THIRD PROMPT****")
    prompt = "give me 10 different jokes, each with a comedy score out of 10. Give it in a JSON format, for example - joke: text, score: score. Do not give me anything other than the JSON response"
    systemRole = "you are a joke creating bot"
    data = get_GPT_response(prompt, systemRole, reponseFormat="json_object")


