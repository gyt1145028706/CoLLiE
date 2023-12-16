import sys
sys.path.append("../../../")

from transformers import AutoTokenizer, GenerationConfig

from collie.models import ChatGLM2ForCausalLM
from collie import  CollieConfig, env

tokenizer = AutoTokenizer.from_pretrained(
        "THUDM/chatglm2-6b",
        trust_remote_code=True,
    )
config = CollieConfig.from_pretrained("THUDM/chatglm2-6b",
        trust_remote_code=True)
config.tp_size = 2
config.pp_size = 4
model = ChatGLM2ForCausalLM.from_pretrained("THUDM/chatglm2-6b", config=config).cuda()
prompt = "[Round 0]\n\n\n\n问：你是谁？\n\n答："
inputs = tokenizer(prompt, return_tensors="pt")
print(inputs)
model.eval()
gen_config = GenerationConfig(max_new_tokens=256, early_stopping=True, eos_token_id=2)

outs = model.generate(inputs["input_ids"].cuda(), generation_config=gen_config)
if env.local_rank == 0:
        print(outs)
        print(tokenizer.decode(outs[0], skip_special_tokens=True))