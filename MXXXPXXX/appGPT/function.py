i=0


def get_model_vocab(cache_dir='/workspace/KoGPT2/kogpt2/', ctx='cpu'):
    import torch
    from gluonnlp.data import SentencepieceTokenizer
    import sys
    import os
    sys.path.append('/workspace/KoGPT2/')
    from kogpt2.utils import get_tokenizer
    from kogpt2.pytorch_kogpt2 import get_pytorch_kogpt2_model
    from model.torch_gpt2 import GPT2Config, GPT2LMHeadModel
    import gluonnlp as nlp
    ctx='cpu'
    
    f_cachedir = os.path.expanduser(cache_dir)
    filename='pytorch_kogpt2_676e9bcfa7.params'
    file_path = os.path.join(f_cachedir, filename)
    model_file=file_path
    
    f_cachedir = os.path.expanduser(cache_dir)
    filename='kogpt2_news_wiki_ko_cased_818bfa919d.spiece'
    file_path = os.path.join(f_cachedir, filename)
    vocab_file=file_path
    
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
    
    kogpt2model=GPT2LMHeadModel(config=GPT2Config.from_dict(kogpt2_config))
    kogpt2model.load_state_dict(torch.load(model_file))
    device=torch.device(ctx)
    kogpt2model.to(device)
    kogpt2model.eval()
    vocab_b_obj=nlp.vocab.BERTVocab.from_sentencepiece(vocab_file,
                                                    mask_token=None,
                                                    sep_token=None,
                                                    cls_token=None,
                                                    unknown_token='<unk>',
                                                    padding_token='<pad>',
                                                    bos_token='<s>',
                                                    eos_token='</s>')

    return kogpt2model, vocab_b_obj
    
    
def get_one_sentence(sent='2019년한해'):
    import torch
    from gluonnlp.data import SentencepieceTokenizer
    import sys
    import os
    sys.path.append('/workspace/KoGPT2/')
    from kogpt2.utils import get_tokenizer


    
    tok_path = get_tokenizer()
    
    tok = SentencepieceTokenizer(tok_path)
    
    cache_dir='/workspace/KoGPT2/kogpt2/'
    model, vocab= get_model_vocab(cache_dir, 'cpu')
    
    
    ''' 학습모델 적용 부분
    load_path = '/content/drive/MyDrive/NarrativeKoGPT2/checkpoint/narrativeKoGPT2_checkpoint_112.tar'
    checkpoint = torch.load(load_path, map_location=device) #튜닝한거 불러오고
    model.load_state_dict(checkpoint['model_state_dict'])  #모델에 적용  
    '''
    
    #sent=''
    toked = tok(sent)
    while 1:
        input_ids = torch.tensor([vocab[vocab.bos_token],]  + vocab[toked]).unsqueeze(0)
        pred = model(input_ids)[0]
        gen = vocab.to_tokens(torch.argmax(pred, axis=-1).squeeze().tolist())[-1]
        if gen == '</s>' or gen=='.':
            print("..")
            break
        sent += gen.replace('▁', ' ')
        toked = tok(sent)
    print(sent)
    return sent
    
#get_one_sentence()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    