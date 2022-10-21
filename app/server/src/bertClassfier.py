import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchtext
# from transformers.modeling_bert import BertModel
from transformers import BertModel
# from transformers.tokenization_bert_japanese import BertJapaneseTokenizer
from transformers import BertJapaneseTokenizer
from transformers import BertModel
# from transformers import BertTokenizer
from transformers import AutoTokenizer
from torchtext.legacy import data
from transformers import BertTokenizer
from transformers import AutoTokenizer


class BertClassifier(nn.Module):
    def __init__(self):
        super(BertClassifier, self).__init__()

        # 日本語学習済モデルをロードする
        # output_attentions=Trueで順伝播のときにattention weightを受け取れるようにする
        # output_hidden_state=Trueで12層のBertLayerの隠れ層を取得する
        self.bert = BertModel.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking',
                                              output_attentions=True,
                                              output_hidden_states=True)

        # BERTの隠れ層の次元数は768だが、最終4層分のベクトルを結合したものを扱うので、７６８×4次元としている。
        self.linear = nn.Linear(768*4, 9)

        # 重み初期化処理
        nn.init.normal_(self.linear.weight, std=0.02)
        nn.init.normal_(self.linear.bias, 0)

    # clsトークンのベクトルを取得する用の関数を用意
    def _get_cls_vec(self, vec):
        return vec[:,0,:].view(-1, 768)

    def forward(self, input_ids):

        # 順伝播の出力結果は辞書形式なので、必要な値のkeyを指定して取得する
        output = self.bert(input_ids)
        attentions = output['attentions']
        hidden_states = output['hidden_states']

        # 最終４層の隠れ層からそれぞれclsトークンのベクトルを取得する
        vec1 = self._get_cls_vec(hidden_states[-1])
        vec2 = self._get_cls_vec(hidden_states[-2])
        vec3 = self._get_cls_vec(hidden_states[-3])
        vec4 = self._get_cls_vec(hidden_states[-4])

        # 4つのclsトークンを結合して１つのベクトルにする。
        vec = torch.cat([vec1, vec2, vec3, vec4], dim=1)

        # 全結合層でクラス分類用に次元を変換
        out = self.linear(vec)

        return F.log_softmax(out, dim=1), attentions
