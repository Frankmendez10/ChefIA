from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer


class LLMService:
    MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

    INTENTS = {
        "RECIPE",
        "SUBSTITUTION",
        "QUESTION",
        "RECOMMENDATION",
    }

    def __init__(self):
        base_path = Path(__file__).resolve().parents[3]

        lora_path = (
            base_path
            / "ai"
            / "fine_tuning"
            / "chefia-lora"
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.MODEL_NAME
        )

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        base_model = AutoModelForCausalLM.from_pretrained(
            self.MODEL_NAME
        )

        self.model = PeftModel.from_pretrained(
            base_model,
            str(lora_path)
        )

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model.to(self.device)

    def classify_intent(self, message: str) -> str:
        text = message.lower().strip()

        substitution_keywords = [
            "sustituir",
            "sustituya",
            "sustituto",
            "reemplazar",
            "reemplazo",
            "alternativa a",
            "en lugar de",
            "puedo usar",
        ]

        question_keywords = [
            "cuánto tiempo",
            "cuanto tiempo",
            "a qué temperatura",
            "a que temperatura",
            "cómo se cocina",
            "como se cocina",
            "cómo cocinar",
            "como cocinar",
            "cuánto tarda",
            "cuanto tarda",
            "qué temperatura",
            "que temperatura",
        ]

        recommendation_keywords = [
            "recomienda",
            "recomiéndame",
            "recomiendame",
            "qué me recomiendas",
            "que me recomiendas",
            "alguna idea",
            "ideas para",
            "quiero una cena",
            "quiero un desayuno",
            "quiero un almuerzo",
            "algo rápido",
            "algo saludable",
        ]

        recipe_keywords = [
            "qué puedo preparar",
            "que puedo preparar",
            "qué puedo cocinar",
            "que puedo cocinar",
            "cómo preparar",
            "como preparar",
            "receta",
            "preparar un",
            "preparar una",
        ]

        if any(keyword in text for keyword in substitution_keywords):
            return "SUBSTITUTION"

        if any(keyword in text for keyword in question_keywords):
            return "QUESTION"

        if any(keyword in text for keyword in recommendation_keywords):
            return "RECOMMENDATION"

        if any(keyword in text for keyword in recipe_keywords):
            return "RECIPE"

        return "QUESTION"

    def generate_response(self, message: str, context: list) -> str:
        context_text = "\n\n".join(
            item["text"]
            for item in context
        )

        prompt = f"""Eres ChefIA, un asistente culinario.

    Información:
    {context_text}

    Usuario:
    {message}

    Responde únicamente con información presente en la sección Información.
    No inventes ingredientes ni sustitutos.
    No hagas preguntas.
    No digas "¡Gracias!".
    No pidas más información.
    Responde en español y de forma breve.

    Respuesta:"""

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt"
        ).to(self.device)

        input_length = inputs["input_ids"].shape[-1]

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=60,
                do_sample=False,
                repetition_penalty=1.15,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        generated_tokens = outputs[0][input_length:]

        answer = self.tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True
        ).strip()

        # Limpiar texto generado
        for marker in [
            "Información:",
            "Usuario:",
            "Respuesta:",
            "CONTEXTO:",
            "PREGUNTA:"
        ]:
            if marker in answer:
                answer = answer.split(marker)[0].strip()

        answer = answer.strip('"').strip()

        return answer