import time

import requests


API_URL = "http://127.0.0.1:8000/api/assistant/chat"

TEST_CASES = [
    {
        "message": "Tengo pollo y arroz, ¿qué puedo preparar?",
        "expected_intent": "RECIPE",
    },
    {
        "message": "¿Con qué puedo sustituir la leche?",
        "expected_intent": "SUBSTITUTION",
    },
    {
        "message": "¿Cuánto tiempo debo cocinar el arroz?",
        "expected_intent": "QUESTION",
    },
    {
        "message": "Quiero una cena rápida y saludable.",
        "expected_intent": "RECOMMENDATION",
    },
    {
        "message": "¿Qué puedo preparar con huevo?",
        "expected_intent": "RECIPE",
    },
    {
        "message": "¿Cuánto tarda la pasta?",
        "expected_intent": "QUESTION",
    },
]


def main():
    correct = 0
    total_time = 0

    print("\n=== ChefIA Evaluation ===\n")

    for test in TEST_CASES:
        start_time = time.time()

        response = requests.post(
            API_URL,
            json={"message": test["message"]},
            timeout=300,
        )

        elapsed = time.time() - start_time
        total_time += elapsed

        result = response.json()

        intent = result["intent"]
        answer = result["answer"]

        is_correct = intent == test["expected_intent"]

        if is_correct:
            correct += 1

        status = "OK" if is_correct else "ERROR"

        print(f"[{status}]")
        print(f"Pregunta: {test['message']}")
        print(f"Intent esperado: {test['expected_intent']}")
        print(f"Intent obtenido: {intent}")
        print(f"Tiempo: {elapsed:.2f} segundos")
        print(f"Respuesta: {answer}")
        print("-" * 60)

    accuracy = correct / len(TEST_CASES) * 100
    average_time = total_time / len(TEST_CASES)

    print(f"\nIntent Accuracy: {accuracy:.1f}%")
    print(f"Correctos: {correct}/{len(TEST_CASES)}")
    print(f"Tiempo promedio: {average_time:.2f} segundos")


if __name__ == "__main__":
    main()