import torch
import re
import sys
sys.path.append('/workspace/KoGPT2/')
print("모듈 적재중... 1/4")
from kogpt2.pytorch_kogpt2 import get_pytorch_kogpt2_model
from gluonnlp.data import SentencepieceTokenizer
from kogpt2.utils import get_tokenizer
print("1")
import os
from kogpt2.utils import get_tokenizer
import gluonnlp as nlp

print("KoGPT2 불러오는중... 2/4")
tok_path = get_tokenizer()
tok = SentencepieceTokenizer(tok_path)
model, vocab = get_pytorch_kogpt2_model()
# ~문장 생성 속도 최적화(2020_05_07_12:00)

print("학습된 파일 모델에 적용중... 3/4")
# 학습된 모델 적용 (2020_05_07_15:02)~
'''
load_path = '/workspace/KoGPT2/checkpoint/narrativeKoGPT2_checkpoint_112.tar'
ctx='cpu'
device = torch.device(ctx)
checkpoint = torch.load(load_path, map_location=device) #튜닝한거 불러오고
model.load_state_dict(checkpoint['model_state_dict'])  #모델에 적용
'''
# ~학습된 모델 적용 (2020_05_07_15:02)

print("서버 준비중... 4/4 한번 더하게됨")


def generate_text(text):
    '''
    tok_path = get_tokenizer()
    model, vocab = get_pytorch_kogpt2_model()
    tok = SentencepieceTokenizer(tok_path)
    '''
    sent = text
    toked = tok(sent)
    while 1:
        input_ids = torch.tensor([
            vocab[vocab.bos_token],
        ] + vocab[toked]).unsqueeze(0)
        pred = model(input_ids)[0]
        gen = vocab.to_tokens(torch.argmax(pred,
                                           axis=-1).squeeze().tolist())[-1]
        if gen == '</s>' or gen == '.':
            break
        sent += gen.replace('▁', ' ')
        toked = tok(sent)
    return sent


def generate_3rd(text):
    '''
    tok_path = get_tokenizer()
    model, vocab = get_pytorch_kogpt2_model()
    tok = SentencepieceTokenizer(tok_path)
    '''

    sent = text
    toked = tok(sent)
    sent_cnt = 0

    input_ids = torch.tensor([
        vocab[vocab.bos_token],
    ] + vocab[toked]).unsqueeze(0)

    outputs = model.generate(input_ids=input_ids,
                             max_length=50,
                             repetition_penalty=1.2,
                             do_sample=True,
                             eos_token_ids=-1,
                             num_return_sequences=3)
    toked = vocab.to_tokens(outputs[0][1].squeeze().tolist())
    ret = re.sub(r'(<s>|</s>)', '', ''.join(toked).replace('▁', ' ').strip())
    return ret
