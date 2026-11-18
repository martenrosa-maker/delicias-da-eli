import httpx
import logging

logger = logging.getLogger("uvicorn")

# Configurações da sua instância na Evolution API
EVOLUTION_API_URL = "http://localhost:8080"  # Altere para a URL do seu servidor Evolution API
EVOLUTION_INSTANCE = "EliConfeitaria"         # Nome da sua instância
API_KEY = "SUA_API_KEY_AQUI"                 # Chave de API configurada na Evolution

class EvolutionService:
    @staticmethod
    async def send_whatsapp_message(phone: str, message: str) -> bool:
        """
        Envia mensagem de texto via Evolution API para um número do WhatsApp.
        """
        # Formata o número (garante apenas dígitos)
        clean_phone = "".join(filter(str.isdigit, phone))
        
        # Adiciona código do país (55) se não houver
        if len(clean_phone) <= 11 and not clean_phone.startswith("55"):
            clean_phone = f"55{clean_phone}"

        endpoint = f"{EVOLUTION_API_URL}/message/sendText/{EVOLUTION_INSTANCE}"
        headers = {
            "apikey": API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "number": clean_phone,
            "options": {
                "delay": 1200,
                "presence": "composing",
                "linkPreview": False
            },
            "textMessage": {
                "text": message
            }
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(endpoint, json=payload, headers=headers)
                
                if response.status_code in (200, 201):
                    logger.info(f"[Evolution API] Mensagem enviada com sucesso para {clean_phone}")
                    return True
                else:
                    logger.error(f"[Evolution API] Erro ({response.status_code}): {response.text}")
                    return False
        except Exception as e:
            logger.error(f"[Evolution API] Exceção ao tentar enviar para {clean_phone}: {str(e)}")
            return False