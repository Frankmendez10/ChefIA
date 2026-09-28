from app.services.llm_service import LLMService
from app.rag.retriever import Retriever


class AssistantService:
    def __init__(self):
        self.llm_service = LLMService()
        self.retriever = Retriever()

    def chat(self, message: str):
        intent = self.llm_service.classify_intent(message)

        context = self.retriever.search(
            message,
            intent=intent
        )

        if intent == "RECOMMENDATION":
            llm_answer = self.llm_service.generate_response(
                message,
                context
            )

            answer = self._build_recommendation_response(
                context,
                llm_answer
            )
        else:
            answer = self._build_rag_response(
                intent,
                context
            )

        return {
            "intent": intent,
            "answer": answer,
        }

    def _build_recommendation_response(
        self,
        context: list,
        llm_answer: str
    ) -> str:
        import json

        if not context:
            return "No encontré una receta adecuada para tu solicitud."

        try:
            data = json.loads(context[0]["text"])

            name = data.get("name", "la receta")
            time = data.get("time_minutes")
            tags = data.get("tags", [])

            response = f"Te recomiendo {name}."

            if time:
                response += (
                    f" Se prepara en aproximadamente {time} minutos."
                )

            if tags:
                relevant_tags = [
                    tag for tag in tags
                    if tag.lower() in [
                        "rápido",
                        "rapido",
                        "saludable",
                        "cena",
                        "desayuno",
                        "almuerzo"
                    ]
                ]

                if relevant_tags:
                    response += (
                        " Es una opción "
                        + ", ".join(relevant_tags)
                        + "."
                    )

                    response = response.replace(
                        "rápido, saludable, cena",
                        "rápida y saludable para la cena"
                    )

            return response

        except (json.JSONDecodeError, TypeError):
            return llm_answer
    def _build_rag_response(self, intent: str, context: list) -> str:
        if not context:
            return "No encontré información suficiente para responder."

        if intent == "SUBSTITUTION":
            data = context[0]["text"]

            return self._format_substitution(data)

        if intent == "QUESTION":
            data = context[0]["text"]

            return self._format_question(data)

        if intent == "RECIPE":
            data = context[0]["text"]

            return self._format_recipe(data)

        return context[0]["text"]

    def _format_substitution(self, text: str) -> str:
        import json

        try:
            data = json.loads(text)

            ingredient = data.get("ingredient", "el ingrediente")
            substitutes = data.get("substitutes", [])

            if not substitutes:
                return f"No encontré sustitutos para {ingredient}."

            options = []

            for substitute in substitutes:
                name = substitute.get("ingredient")
                ratio = substitute.get("ratio")

                if name and ratio:
                    options.append(f"{name} ({ratio})")
                elif name:
                    options.append(name)

            return (
                f"Puedes sustituir {ingredient} por "
                + ", ".join(options)
                + "."
            )

        except (json.JSONDecodeError, TypeError):
            return text

    def _format_question(self, text: str) -> str:
        import json

        try:
            data = json.loads(text)

            return data.get("content", text)

        except (json.JSONDecodeError, TypeError):
            return text

    def _format_recipe(self, text: str) -> str:
        import json

        try:
            data = json.loads(text)

            name = data.get("name", "la receta")
            time = data.get("time_minutes")
            ingredients = data.get("ingredients", [])

            response = f"Puedes preparar {name}."

            if ingredients:
                response += (
                    " Sus ingredientes principales son "
                    + ", ".join(ingredients)
                    + "."
                )

            if time:
                response += f" El tiempo de preparación es de aproximadamente {time} minutos."

            return response

        except (json.JSONDecodeError, TypeError):
            return text