from app.rag.retriever import Retriever


def test_recipe_retrieval():
    retriever = Retriever()

    results = retriever.search(
        "Tengo pollo y arroz, ¿qué puedo preparar?",
        intent="RECIPE"
    )

    assert len(results) > 0

    assert any(
        "Arroz con pollo" in result["text"]
        for result in results
    )


def test_substitution_retrieval():
    retriever = Retriever()

    results = retriever.search(
        "¿Con qué puedo sustituir la leche?",
        intent="SUBSTITUTION"
    )

    assert len(results) > 0

    assert any(
        '"ingredient": "leche"' in result["text"]
        for result in results
    )


def test_question_retrieval():
    retriever = Retriever()

    results = retriever.search(
        "¿Cuánto tiempo debo cocinar el arroz?",
        intent="QUESTION"
    )

    assert len(results) > 0

    assert any(
        "arroz" in result["text"].lower()
        for result in results
    )


def test_recommendation_retrieval():
    retriever = Retriever()

    results = retriever.search(
        "Quiero una cena rápida y saludable.",
        intent="RECOMMENDATION"
    )

    assert len(results) > 0

    assert any(
        "Ensalada de pollo rápida" in result["text"]
        for result in results
    )