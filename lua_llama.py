import requests
from huggingface_hub import InferenceClient
import time

# Configurações para o modelo LLaMA
llama_client = InferenceClient(
    "meta-llama/Meta-Llama-3-8B-Instruct",
    token="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"
)

def gerar_resposta_llama(prompt, historico=None):
    """Gera uma resposta para o prompt dado usando o modelo LLaMA."""
    
    # Instruções para resposta breve se o prompt incluir "{f:}"
    if prompt.startswith("Por favor, me dê uma resposta breve e precisa:"):
        messages = [{"role": "user", "content": prompt}]
    else:
        messages = [{"role": "user", "content": prompt}]
    
    retries = 5
    delay = 60  # Tempo de espera em segundos

    for attempt in range(retries):
        try:
            response_generator = llama_client.chat_completion(
                messages=messages,
                max_tokens=500,
                stream=False
            )
            resposta = response_generator.choices[0].message.content
            return resposta
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print(f"Rate limit atingido. Tentando novamente em {delay} segundos...")
                time.sleep(delay)
                continue
            else:
                raise  # Propaga outros erros
        except Exception as e:
            print(f"Erro ao gerar resposta: {e}")
            break
    return "Desculpe, não consegui gerar uma resposta no momento."
