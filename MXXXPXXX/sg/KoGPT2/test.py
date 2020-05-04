import torch
import re
from .kogpt2.pytorch_kogpt2 import get_pytorch_kogpt2_model
from gluonnlp.data import SentencepieceTokenizer
from .kogpt2.utils import get_tokenizer

def generate_text(text):
  tok_path = get_tokenizer()
  model, vocab = get_pytorch_kogpt2_model()
  tok = SentencepieceTokenizer(tok_path)
  sent = text
  toked = tok(sent)
  while 1:
    input_ids = torch.tensor([vocab[vocab.bos_token],]  + vocab[toked]).unsqueeze(0)
    pred = model(input_ids)[0]
    gen = vocab.to_tokens(torch.argmax(pred, axis=-1).squeeze().tolist())[-1]
    if gen == '</s>':
        break
    sent += gen.replace('▁', ' ')
    toked = tok(sent)
  return sent

def generate_3rd(text):
  tok_path = get_tokenizer()
  model, vocab = get_pytorch_kogpt2_model()
  tok = SentencepieceTokenizer(tok_path)

  sent = text
  toked = tok(sent)
  sent_cnt = 0

  input_ids = torch.tensor([vocab[vocab.bos_token],]  + vocab[toked]).unsqueeze(0)

  outputs = model.generate(input_ids=input_ids, max_length=50, repetition_penalty=1.2, do_sample=True, eos_token_ids=-1, num_return_sequences=3)
  toked = vocab.to_tokens(outputs[0][1].squeeze().tolist())
  ret = re.sub(r'(<s>|</s>)', '' , ''.join(toked).replace('▁', ' ').strip())
  return ret
