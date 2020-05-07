i = 0
# 성구형 문장생성있어서 서버 시작 준비시간 단축하기위해 주석처리 2020_05_07_12:16
'''
print("123")
import torch
from gluonnlp.data import SentencepieceTokenizer
import sys
import os
sys.path.append('/workspace/KoGPT2/')
from kogpt2.utils import get_tokenizer
from kogpt2.pytorch_kogpt2 import get_pytorch_kogpt2_model
from model.torch_gpt2 import GPT2Config, GPT2LMHeadModel
import gluonnlp as nlp




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
print("456")
model, vocab = get_model_vocab()
print("서버 준비 완료 sw")
    
def get_one_sentence(sent='2019년한해'):

    ret = get_one_sentence_sub(model, vocab, sent)

    return ret
    
def get_one_sentence_sub(model, vocab, sent):
    
    toked = tok(sent)
    while 1:
        input_ids = torch.tensor([
            vocab[vocab.bos_token],
        ] + vocab[toked]).unsqueeze(0)
        pred = model(input_ids)[0]
        gen = vocab.to_tokens(torch.argmax(pred,
                                           axis=-1).squeeze().tolist())[-1]
        if gen == '</s>' or gen == '.':
            print("..")
            break
        sent += gen.replace('▁', ' ')
        toked = tok(sent)
    print(sent)
    return sent
'''
    
    
