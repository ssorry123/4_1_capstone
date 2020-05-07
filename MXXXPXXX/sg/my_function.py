import torch
import re
import sys
sys.path.append('/workspace/KoGPT2/')
from kogpt2.pytorch_kogpt2 import get_pytorch_kogpt2_model
from gluonnlp.data import SentencepieceTokenizer
from kogpt2.utils import get_tokenizer
print("1")
import os
from kogpt2.utils import get_tokenizer
from model.torch_gpt2 import GPT2Config, GPT2LMHeadModel
import gluonnlp as nlp

# 문장 생성 속도 최적화(2020_05_07_12:00)~
# 처음 서버 실행이 오래걸리지만 처음만 오래걸림

def get_model_vocab(cache_dir='/workspace/KoGPT2/kogpt2/', ctx='cpu'):

    ctx = 'cpu'

    f_cachedir = os.path.expanduser(cache_dir)
    filename = 'pytorch_kogpt2_676e9bcfa7.params'
    file_path = os.path.join(f_cachedir, filename)
    model_file = file_path

    f_cachedir = os.path.expanduser(cache_dir)
    filename = 'kogpt2_news_wiki_ko_cased_818bfa919d.spiece'
    file_path = os.path.join(f_cachedir, filename)
    vocab_file = file_path

    kogpt2_config = {
        "initializer_range": 0.02,
        "layer_norm_epsilon": 1e-05,
        "n_ctx": 1024,
        "n_embd": 768,
        "n_head": 12,
        "n_layer": 12,
        "n_positions": 1024,
        "vocab_size": 50000
    }

    kogpt2model = GPT2LMHeadModel(config=GPT2Config.from_dict(kogpt2_config))
    kogpt2model.load_state_dict(torch.load(model_file))
    device = torch.device(ctx)
    kogpt2model.to(device)
    kogpt2model.eval()
    vocab_b_obj = nlp.vocab.BERTVocab.from_sentencepiece(vocab_file,
                                                         mask_token=None,
                                                         sep_token=None,
                                                         cls_token=None,
                                                         unknown_token='<unk>',
                                                         padding_token='<pad>',
                                                         bos_token='<s>',
                                                         eos_token='</s>')

    return kogpt2model, vocab_b_obj

tok_path = get_tokenizer()
tok = SentencepieceTokenizer(tok_path)
model, vocab = get_model_vocab()
print("서버 준비 완료 sg")
# ~문장 생성 속도 최적화(2020_05_07_12:00)

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
        if gen == '</s>':
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
