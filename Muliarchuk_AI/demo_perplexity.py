import os
from dotenv import load_dotenv
from perplexity_package import perplexity_module

def main():
    load_dotenv()
    
    api_key = perplexity_module.GetApiKey()
    if api_key.startswith("Error:"):
        print("Помилка: API ключ не знайдено")
        return
    
    print("\nЗапит українською:")
    ua_query = "Що таке штучний інтелект? Дай коротку відповідь."
    print(f"Питання: {ua_query}\n")
    
    ua_result = perplexity_module.GetTokenUsage(ua_query)
    if "error" not in ua_result:
        print(f"Відповідь: {ua_result['response']}\n")
        print(f"Токенів запит: {ua_result['prompt_tokens']}")
        print(f"Токенів відповідь: {ua_result['completion_tokens']}")
        print(f"Вартість: ${ua_result['total_cost_usd']:.6f}")
    
    print("\n" + "="*50)
    print("\nЗапит англійською:")
    en_query = "What is artificial intelligence? Give a brief answer."
    print(f"Питання: {en_query}\n")
    
    en_result = perplexity_module.GetTokenUsage(en_query)
    if "error" not in en_result:
        print(f"Відповідь: {en_result['response']}\n")
        print(f"Токенів запит: {en_result['prompt_tokens']}")
        print(f"Токенів відповідь: {en_result['completion_tokens']}")
        print(f"Вартість: ${en_result['total_cost_usd']:.6f}")


if __name__ == "__main__":
    main()
