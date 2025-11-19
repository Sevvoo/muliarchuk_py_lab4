import os
from typing import Optional
from openai import OpenAI


def GetApiKey() -> str:
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "Error: ключ не знайдено"
        return api_key
    except Exception as e:
        return f"Error: {str(e)}"


def SendQuery(query: str, model: str = "gpt-3.5-turbo") -> str:
    try:
        api_key = GetApiKey()
        if api_key.startswith("Error:"):
            return api_key
        
        client = OpenAI(api_key=api_key)
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ]
        
        response = client.chat.completions.create(model=model, messages=messages)
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


def GetTokenUsage(query: str, model: str = "gpt-3.5-turbo") -> dict:
    try:
        api_key = GetApiKey()
        if api_key.startswith("Error:"):
            return {"error": api_key}
        
        client = OpenAI(api_key=api_key)
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ]
        
        response = client.chat.completions.create(model=model, messages=messages)
        usage = response.usage
        
        prompt_cost = (usage.prompt_tokens / 1_000_000) * 0.50
        completion_cost = (usage.completion_tokens / 1_000_000) * 1.50
        
        return {
            "response": response.choices[0].message.content,
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
            "total_cost_usd": round(prompt_cost + completion_cost, 6),
            "model": model
        }
    except Exception as e:
        return {"error": f"Error: {str(e)}"}


def CalculateTokenCost(prompt_tokens: int, completion_tokens: int, model: str = "gpt-3.5-turbo") -> str:
    try:
        prompt_cost = (prompt_tokens / 1_000_000) * 0.50
        completion_cost = (completion_tokens / 1_000_000) * 1.50
        total = prompt_cost + completion_cost
        
        return f"Токени: {prompt_tokens + completion_tokens}, Вартість: ${total:.6f}"
    except Exception as e:
        return f"Error: {str(e)}"


def FormatResponse(usage_data: dict) -> str:
    try:
        if "error" in usage_data:
            return usage_data["error"]
        
        result = f"{usage_data['response']}\n\n"
        result += f"Токенів: {usage_data['total_tokens']}, "
        result += f"Вартість: ${usage_data['total_cost_usd']:.6f}"
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"
