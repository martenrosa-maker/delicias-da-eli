import os
import requests
import logging
from pathlib import Path
from dotenv import load_dotenv

# Carregamento garantido do .env na raiz C:\marten_smart\.env
BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path, override=True)

logger = logging.getLogger("uvicorn")

class EvolutionService:
    @staticmethod
    def send_whatsapp_message(
        to_phone: str, 
        client_name: str = "Cliente", 
        event_name: str = "Evento Especial", 
        event_date: str = "breve", 
        custom_message: str = "",
        template_name: str = "lembrete_evento", 
        language_code: str = "pt_BR"
    ) -> dict:
        """
        Envia mensagem via Meta Cloud API utilizando o Template Aprovado no Gerenciador do WhatsApp.
        Atende à exigência de 3 parâmetros para o modelo 'lembrete_evento' ({{1}}, {{2}}, {{3}}).
        """
        try:
            phone_id = os.getenv("WHATSAPP_PHONE_ID")
            token = os.getenv("WHATSAPP_TOKEN")

            if not phone_id or not token:
                msg_err = f"Credenciais ausentes no .env (Verificado em: {env_path})"
                logger.error(f"[WhatsAppService] {msg_err}")
                return {"success": False, "error": msg_err}

            # 1. Sanitização do número de telefone com DDI do Brasil (55)
            clean_phone = "".join(filter(str.isdigit, str(to_phone)))
            if len(clean_phone) in [10, 11]:
                clean_phone = f"55{clean_phone}"

            url = f"https://graph.facebook.com/v18.0/{phone_id}/messages"
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }

            # Se custom_message contiver texto gerado por IA, usamos ele como primeiro parâmetro ou usamos os dados individuais
            param1 = client_name if client_name else "Cliente"
            param2 = event_name if event_name else "Bolo / Doce Especial"
            param3 = event_date if event_date else "nos próximos dias"

            # 2. Estrutura de Payload com EXATAMENTE 3 PARÂMETROS exigidos pela Meta
            payload = {
                "messaging_product": "whatsapp",
                "to": clean_phone,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {
                        "code": language_code
                    },
                    "components": [
                        {
                            "type": "body",
                            "parameters": [
                                {
                                    "type": "text",
                                    "text": str(param1)  # Preenche {{1}}
                                },
                                {
                                    "type": "text",
                                    "text": str(param2)  # Preenche {{2}}
                                },
                                {
                                    "type": "text",
                                    "text": str(param3)  # Preenche {{3}}
                                }
                            ]
                        }
                    ]
                }
            }

            logger.info(f"[WhatsAppService] Disparando template '{template_name}' com 3 parâmetros para {clean_phone}...")
            response = requests.post(url, json=payload, headers=headers, timeout=12)
            
            try:
                response_data = response.json()
            except Exception:
                response_data = {"raw_text": response.text}

            if response.status_code in [200, 201]:
                logger.info(f"[WhatsAppService] Mensagem enviada com sucesso para {clean_phone}")
                return {"success": True, "data": response_data}
            else:
                logger.error(f"[WhatsAppService] Erro na Meta Cloud API ({response.status_code}): {response_data}")
                return {"success": False, "error": response_data}

        except Exception as e:
            logger.error(f"[WhatsAppService] Exceção crítica ao disparar WhatsApp: {str(e)}")
            return {"success": False, "error": str(e)}

    @staticmethod
    def send_event_reminder(to_phone: str, message: str = "", *args, **kwargs) -> dict:
        """
        Método utilitário flexível mantido para compatibilidade com o event_service.py
        """
        # Extrai os dados se forem passados como argumentos ou utiliza a mensagem como param1
        client_name = kwargs.get("client_name", message if message else "Cliente")
        event_name = kwargs.get("event_name", "Aniversário / Festa")
        event_date = kwargs.get("event_date", "esta semana")

        return EvolutionService.send_whatsapp_message(
            to_phone=to_phone, 
            client_name=client_name, 
            event_name=event_name, 
            event_date=event_date,
            custom_message=message
        )