#version 2020_05_16(1st)
print('sw_gpt_function.py loading')

'''
    1. 기본 package
'''

import os
import sys
import random
import torch
from gluonnlp.data import SentencepieceTokenizer
import re


'''
    2. KoGPT2 package
'''
# local마다 import 방법이 상의할 수 있음(이름 지정) 각자 컴퓨터에 맞게
# 나중에 기회되면 통일하기로
sys.path.append('/workspace/KoGPT2/')
from kogpt2.utils import get_tokenizer
from kogpt2.pytorch_kogpt2 import get_pytorch_kogpt2_model


'''
3. 함수에서 사용할 전역변수 tok_path, tok, model, vocab
'''
# sk에서 제공하는 50000단어 모델로 변수 설정
# 문장 속도 최적화를 위해, 서버 실행시 전역 변수로 사용하기 위해서
# django App 생성 후 그 폴더 내부에 저장
# @@@views.py에 import 하면 이 파일은 서버 실행 될때 실행된다.@@@
# (app내부가 아닌 py 파일은 서버 실행시 모두 실행되지 않음)
tok_path = get_tokenizer()
tok = SentencepieceTokenizer(tok_path)

# 1) model, vocab 파일의 경우 setup.py 실행시
# kogpt2가 파이썬 내장 모듈로 설정되어 파이썬 설치 경로에 존재
# 2) sys.path.append('~~~')로 폴더를 직접 추가 한 경우
# 파이썬이 사용자 폴더를 참조, 사용자 폴더에 존재
# 3) 한번 다운로드 후 특별한 일이 없는 한 다운하지 않고
# 다운되어 있는 파일을 사용 (using cached model)
model, vocab = get_pytorch_kogpt2_model()


'''
#   4. fine turning한 것을 모델에 적용하기
'''
# 미적용


'''
    5. 정의된 함수들
    단어 추천 함수 : words_list, context_words_list,
    문장 생성 함수 : step_by_step_generate,  oneQ_generate_rd,  oneQ_generate
    확률 계산은 모르겠다.
    ***주의사항***
    @@@!!! 모두 장고에 맞게 추후 수정 필요!!!@@@
    (추천 단어 보여주기,,, 실시간 사용자의 단어 입력 받고 처리 하기 등등..)
    (터미널에서 이루어지기 때문에 서버 실행 전에는 비활성화하고 실험할때만.)
'''

# kogpt2 단어 예측의 경우 마지막 단어만 이용하여 예측하는 것이 아님
# 지금까지 입력된 모든 단어들을 이용하여 다음 단어 예측
# 즉 '중국의'+'경제개혁은' -> '시진핑'을 가장 추천
# '경제개혁은' -> '시진핑'이 아닌 다른 단어를 추천
# 그러나 문맥에 상관 없이 한 단어 or 끝나지 않은 문장을 입력했을때에도
# 다음 단어를 추천해 줄 수 있는 함수를 만듬 필요없지만 필요할수도 있을거 같아서
# 한 단어에 대한 다음 단어 추천 words 는 str, ret은 list{str}
def words_list(words):
    ret = list()
    toked=tok(words)
    cnt=len(toked)-1
    input_ids=torch.tensor([vocab[vocab.bos_token],] + vocab[toked]).unsqueeze(0)
    pred = model(input_ids)[0]
    print(cnt)
    sort=torch.argsort(-pred, axis=-1)[0]
    for i in range(0,10):
        a=sort[cnt][i].squeeze().tolist()
        b=sort[cnt+1][i].squeeze().tolist()
        gen=vocab.to_tokens([b])
        ret.append(gen)

    return ret
# 예시
print(words_list('중국은'))


# 문맥에 맞는 추천 단어 생성
# 위 words_list와 다르게 문맥을 전달해주어야함
# pred = 단순 str이 아닌 model 변수, ret은 list{str}
def context_words_list(pred, toked):
    ret = list()  # 추천 단어를 담을 list
    _pred=pred    # 전달 받은 입력된 단어들,문맥
    cnt=len(toked)-1    # 여러 단어를 입력했을 수 있으므로 반드시 필요
    
    sort=torch.argsort(-_pred, axis=-1)[0]  # 확률이 큰 기준으로 정렬
    for i in range(0,10):
        a=sort[cnt][i].squeeze().tolist()
        b=sort[cnt+1][i].squeeze().tolist()
        gen=vocab.to_tokens([b])    # 하나의 추천 단어
        ret.append(gen)

    return ret


# 문맥에 맞는 추천 단어 생성 함수(context_words_list())를 사용
# default '중국은'
def step_by_step_generate(sent = '중국은'):
    sent = input('입력 :: ')
    toked=tok(sent)
    
    while 1:
        input_ids=torch.tensor([vocab[vocab.bos_token],] + vocab[toked]).unsqueeze(0)
        pred = model(input_ids)[0]
        
        # 추천 단어 보여주기, 문맥 적용
        print(context_words_list(pred, toked))
        
        # 입력은 사용자가 하고 싶은거 하기
        # _은 스페이스바임. 추천그대로 하려면 반드시 입력할것
        gen = input('입력 :: ')
        
        # 사용자가 !end를 입력한경우 종료되게 설정
        if gen == '!end' or gen == '</s>':
            print('end')
            break;
        
        sent += gen.replace('▁', ' ')
        toked=tok(sent)
        
    print(sent)
        
#step_by_step_generate()


# 이 함수는 한 문장이나 단어가 들어오면
# generate함수로 다이렉트로 1개이상의 문장을 만들어낸다.
# 따라서 추천 단어를 사용할 수 없다.
# return은 str의 리스트
def oneQ_generate_rd(sent = '일본은', generate_num=3):
    #sent = input('입력 : ')
    ret_list = list()
    toked=tok(sent)
    input_ids = torch.tensor([vocab[vocab.bos_token],] + vocab[toked]).unsqueeze(0)
    
    # do_sample True 랜덤 생성
    # num_return_sequences 생성할 문장 개수
    
    outputs = model.generate(input_ids=input_ids,
                             max_lenght=160,
                             repetition_penalty=1.2,
                             do_sample=True,
                            num_return_sequences = generate_num)
    
    for i in range(generate_num):
        toked = vocab.to_tokens(ouputs[0][i].squeeze().tolist())
        ret = re.sub(r'(<s>|</s>)', '' , ''.join(toked).replace('▁', ' ').strip())
        ret_list.append(ret)
        
    return ret_list
    
    
# 단어가 들어오면
# generate함수로 다이렉트로 1 문장을 만들어낸다.
# 성구형거와 다 같음 단지 3에서 1로 변했을뿐
def oneQ_generate(sent = '일본은'):
    #sent = input('입력 : ')

    sent = text
    toked = tok(sent)
    sent_cnt = 0

    input_ids = torch.tensor([vocab[vocab.bos_token],] + vocab[toked]).unsqueeze(0)

    outputs = model.generate(input_ids=input_ids,
                             max_length=50,
                             repetition_penalty=1.2,
                             do_sample=True,
                             eos_token_ids=-1,
                             num_return_sequences=1)
    
    toked = vocab.to_tokens(outputs[0][1].squeeze().tolist())
    ret = re.sub(r'(<s>|</s>)', '', ''.join(toked).replace('▁', ' ').strip())
        
    return ret
    
    