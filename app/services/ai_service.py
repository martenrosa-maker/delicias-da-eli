import os
import logging
from google import genai

logger = logging.getLogger("uvicorn")

class AIService:
    @staticmethod
    async def generate_reminder_message(client_name: str, event_name: str, event_date: str) -> str:
        """
        Gera a mensagem via Gemini com Fallback garantido para produção.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        
        # Mensagem Padrão de Alta Qualidade (Fallback)
        default_message = (
            f"Olá, {client_name}! 🍰 Passando para lembrar do seu evento '{event_name}' "
            f"agendado para o dia {event_date}. Qualquer dúvida sobre o seu pedido, "
            f"estamos à disposição na Delícias da Eli! ✨"
        )

        if not api_key:
            logger.warning("[AIService] GEMINI_API_KEY ausente. Usando mensagem padrão.")
            return default_message

        try:
            client = genai.Client(api_key=api_key)
            prompt = (
                f"Escreva uma mensagem curta, carinhosa e profissional pelo WhatsApp para a cliente {client_name}, "
                f"lembrando do evento '{event_name}' no dia {event_date}. "
                f"O negócio é uma confeitaria/doceria artesanal chamada 'Delícias da Eli'. Inclua emojis."
            )
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            
            if response and response.text:
                return response.text.strip()
            return default_message

        except Exception as e:
            logger.error(f"[AIService] Falha ao comunicar com Gemini: {str(e)}. Aplicando fallback.")
            return default_message