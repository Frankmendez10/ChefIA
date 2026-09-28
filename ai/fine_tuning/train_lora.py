import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
)
from peft import LoraConfig
from trl import SFTTrainer


MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

dataset = load_dataset(
    "json",
    data_files="../../ai/dataset/chefia_lora.json",
    split="train"
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32
)

def format_example(example):
    return (
        f"### Instrucción:\n"
        f"{example['instruction']}\n\n"
        f"### Respuesta:\n"
        f"{example['response']}"
    )

lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj"
    ],
)

training_args = TrainingArguments(
    output_dir="./chefia-lora",
    num_train_epochs=1,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=1,
    learning_rate=2e-4,
    logging_steps=1,
    save_strategy="no",
    report_to="none",
    fp16=False,
)

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=lora_config,
    formatting_func=format_example,
    args=training_args,
)

trainer.train()

trainer.save_model("./chefia-lora")
tokenizer.save_pretrained("./chefia-lora")

print("LoRA training terminado.")