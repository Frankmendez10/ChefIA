import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


class Retriever:
    def __init__(self):
        base_path = Path(__file__).resolve().parents[3]

        self.model = SentenceTransformer(
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )

        self.documents = self._load_documents(base_path)

        texts = [
            document["text"]
            for document in self.documents
        ]

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True
        )

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

    def _load_documents(self, base_path: Path):
        documents = []

        files = [
            base_path / "data" / "recipes" / "recipes.json",
            base_path / "data" / "knowledge" / "ingredients.json",
            base_path / "data" / "knowledge" / "substitutions.json",
            base_path / "data" / "knowledge" / "cooking_knowledge.json",
        ]

        for file_path in files:
            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

            for item in data:
                documents.append({
                    "source": file_path.name,
                    "text": json.dumps(
                        item,
                        ensure_ascii=False
                    ),
                    "data": item
                })

        return documents

    def search(
        self,
        query: str,
        intent: str = None,
        top_k: int = 3
    ):
        if intent == "RECOMMENDATION":
            return self._search_recommendations(
                query,
                top_k
            )

        if intent == "RECIPE":
            return self._search_recipes(
                query,
                top_k
            )

        if intent == "SUBSTITUTION":
            return self._search_substitutions(
                query,
                top_k
            )

        # QUESTION
        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )

        scores, indices = self.index.search(
            query_embedding,
            len(self.documents)
        )

        allowed_sources = [
            "cooking_knowledge.json",
            "ingredients.json"
        ]

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):
            if index == -1:
                continue

            document = self.documents[index]

            if document["source"] not in allowed_sources:
                continue

            results.append({
                "score": float(score),
                "source": document["source"],
                "text": document["text"]
            })

            if len(results) >= top_k:
                break

        return results

    def _search_recipes(
        self,
        query: str,
        top_k: int = 3
    ):
        query_lower = query.lower()

        matches = []

        for document in self.documents:
            if document["source"] != "recipes.json":
                continue

            recipe = document["data"]

            score = 0

            # Nombre de la receta
            name = recipe.get(
                "name",
                ""
            ).lower()

            if name and name in query_lower:
                score += 10

            # Ingredientes mencionados
            ingredients = [
                ingredient.lower()
                for ingredient in recipe.get(
                    "ingredients",
                    []
                )
            ]

            for ingredient in ingredients:
                if ingredient in query_lower:
                    score += 3

            # Tipo de comida
            meal = recipe.get(
                "meal",
                ""
            ).lower()

            if meal and meal in query_lower:
                score += 4

            # Tags
            tags = [
                tag.lower()
                for tag in recipe.get(
                    "tags",
                    []
                )
            ]

            for tag in tags:
                if tag in query_lower:
                    score += 2

            if score > 0:
                matches.append({
                    "score": score,
                    "source": document["source"],
                    "text": document["text"]
                })

        matches.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return matches[:top_k]

    def _search_substitutions(
        self,
        query: str,
        top_k: int = 3
    ):
        query_lower = query.lower()

        matches = []

        for document in self.documents:
            if document["source"] != "substitutions.json":
                continue

            data = document["data"]

            ingredient = data.get(
                "ingredient",
                ""
            ).lower()

            if not ingredient:
                continue

            score = 0

            if ingredient in query_lower:
                score += 10

            # También considerar sustitutos mencionados
            for substitute in data.get(
                "substitutes",
                []
            ):
                substitute_name = substitute.get(
                    "ingredient",
                    ""
                ).lower()

                if substitute_name in query_lower:
                    score += 3

            if score > 0:
                matches.append({
                    "score": score,
                    "source": document["source"],
                    "text": document["text"]
                })

        matches.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return matches[:top_k]

    def _search_recommendations(
        self,
        query: str,
        top_k: int = 3
    ):
        query_lower = query.lower()

        matches = []

        for document in self.documents:
            if document["source"] != "recipes.json":
                continue

            recipe = document["data"]

            score = 0

            # Tipo de comida
            meal = recipe.get(
                "meal",
                ""
            ).lower()

            if "cena" in query_lower and meal == "cena":
                score += 5

            if "desayuno" in query_lower and meal == "desayuno":
                score += 5

            if "almuerzo" in query_lower and meal == "almuerzo":
                score += 5

            # Tags
            tags = [
                tag.lower()
                for tag in recipe.get(
                    "tags",
                    []
                )
            ]

            if (
                "rápida" in query_lower
                or "rapida" in query_lower
            ):
                if (
                    "rápido" in tags
                    or "rapido" in tags
                ):
                    score += 4

            if "saludable" in query_lower:
                if "saludable" in tags:
                    score += 4

            # Tiempo
            if (
                "rápida" in query_lower
                or "rapida" in query_lower
            ):
                if recipe.get(
                    "time_minutes",
                    999
                ) <= 20:
                    score += 3

            # Ingredientes mencionados
            ingredients = [
                ingredient.lower()
                for ingredient in recipe.get(
                    "ingredients",
                    []
                )
            ]

            for ingredient in ingredients:
                if ingredient in query_lower:
                    score += 3

            if score > 0:
                matches.append({
                    "score": score,
                    "source": document["source"],
                    "text": document["text"]
                })

        matches.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return matches[:top_k]