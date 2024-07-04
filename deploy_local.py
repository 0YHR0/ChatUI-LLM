import torch
import transformers
from torch import cuda, bfloat16
import yaml
from transformers import StoppingCriteria, StoppingCriteriaList

'''
Load the config and check the devices

'''
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

parameters = config['Parameters']
top_k = parameters['Top_k']
top_p = parameters['Top_p']
temperature = parameters['Temperature']
max_new_tokens = parameters['Max_New_Tokens']

model_name = config['Local_Deploy']['Model_Name']

device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'
print(device)

model = transformers.AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = transformers.AutoTokenizer.from_pretrained(model_name, use_fast=False)

tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

model.eval()
model.to(device)
print(f"Model loaded on {device}")

'''
Stop tokens

'''
___inst = tokenizer.convert_ids_to_tokens(tokenizer("<|begin_of_text|>")["input_ids"])[1:]
# ___java = tokenizer.convert_ids_to_tokens(tokenizer("```java")["input_ids"])#[1:]
___start_of_ = tokenizer.convert_ids_to_tokens(tokenizer("<|start_header_id|>")["input_ids"])[1:]
___eot = tokenizer.convert_ids_to_tokens(tokenizer("<|eot_id|>")["input_ids"])[1:]
___end_of = tokenizer.convert_ids_to_tokens(tokenizer("<|end_of_text|>")["input_ids"])[1:]
# ___hash_tag = tokenizer.convert_ids_to_tokens(tokenizer("#")["input_ids"])[1:]
# ___star = tokenizer.convert_ids_to_tokens(tokenizer("*")["input_ids"])[1:]

stop_token_ids = [
    tokenizer.convert_tokens_to_ids(x) for x in
    [___inst, ___start_of_, [tokenizer.eos_token], ___end_of, ___eot, ['```']]
]

stop_token_ids = [torch.LongTensor(x).to(device) for x in stop_token_ids]


class StopOnTokens(StoppingCriteria):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        for stop_ids in stop_token_ids:
            if torch.eq(input_ids[0][-len(stop_ids):], stop_ids).all():
                return True
        return False


stopping_criteria = StoppingCriteriaList([StopOnTokens()])

'''
Access the model

'''
pipe = transformers.pipeline(
    model=model,
    tokenizer=tokenizer,
    return_full_text=True,  # Set it to True when combining with LangChain
    task='text-generation',
    device=device,
    stopping_criteria=stopping_criteria,
    temperature=temperature,
    top_p=top_p,
    top_k=top_k,
    max_new_tokens=max_new_tokens,
    repetition_penalty=1.3
)


def request_local_llm(message):
    result = pipe(message)
    return result[0]['generated_text']