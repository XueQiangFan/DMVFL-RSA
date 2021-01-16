#!/Users/11834/.conda/envs/Pytorch_GPU/python.exe
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File    ：FWorks -> BiLSTM_SE_Net
@IDE    ：PyCharm
@Date   ：2020/12/6 10:53
=================================================='''
import torch.nn as nn
import torch
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)
class SELayer(nn.Module):
    def __init__(self, channel, reduction=16):
        super(SELayer, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool1d(channel)
        self.fc = nn.Sequential(
            nn.Linear(channel, channel // reduction, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(channel // reduction, channel, bias=False),
            nn.Sigmoid())

    def forward(self, x):
        y = self.avg_pool(x)
        y = self.fc(y)
        return x * y.expand_as(x)


class LSTMMergeSE(nn.Module):

    def __init__(self, num_layers=2, input_features_0=300, hidden_dim_0=256, input_features_1=300, hidden_dim_1=256,
                 input_features_2=45, hidden_dim_2=32):
        super(LSTMMergeSE, self).__init__()
        self.input_features_0 = input_features_0
        self.hidden_dim_0 = hidden_dim_0
        self.input_features_1 = input_features_1
        self.hidden_dim_1 = hidden_dim_1
        self.input_features_2 = input_features_2
        self.hidden_dim_2 = hidden_dim_2
        self.num_layers = num_layers
        self.lstm00 = nn.LSTM(input_size=self.input_features_0, hidden_size=self.hidden_dim_0,
                              num_layers=self.num_layers,
                              dropout=0.5, batch_first=True, bidirectional=True)
        self.lstm01 = nn.LSTM(input_size=self.hidden_dim_0 * 2, hidden_size=self.hidden_dim_0 * 2,
                              num_layers=self.num_layers,
                              dropout=0.5, batch_first=True, bidirectional=True)

        self.SELayer00 = SELayer(1024)
        self.fc00 = nn.Sequential(
            nn.Linear(1024, 512),
            nn.BatchNorm1d(512),
            nn.Tanh(),
            nn.Dropout(0.5),
        )
        self.SELayer01 = SELayer(512)
        self.fc01 = nn.Sequential(
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.Tanh(),
            nn.Dropout(0.5),
            nn.Linear(256, 1)
        )


        self.lstm10 = nn.LSTM(input_size=self.input_features_1, hidden_size=self.hidden_dim_1,
                              num_layers=self.num_layers,
                              dropout=0.5, batch_first=True, bidirectional=True)
        self.lstm11 = nn.LSTM(input_size=self.hidden_dim_1 * 2, hidden_size=self.hidden_dim_1 * 2,
                              num_layers=self.num_layers,
                              dropout=0.5, batch_first=True, bidirectional=True)
        self.SELayer10 = SELayer(1024)
        self.fc10 = nn.Sequential(
            nn.Linear(1024, 512),
            nn.BatchNorm1d(512),
            nn.Tanh(),
            nn.Dropout(0.5),
        )
        self.SELayer11 = SELayer(512)
        self.fc11 = nn.Sequential(
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.Tanh(),
            nn.Dropout(0.5),
            nn.Linear(256, 1)
        )


        self.lstm20 = nn.LSTM(input_size=self.input_features_2, hidden_size=self.hidden_dim_2,
                              num_layers=self.num_layers,
                              dropout=0.5, batch_first=True, bidirectional=True)
        self.lstm21 = nn.LSTM(input_size=self.hidden_dim_2 * 2, hidden_size=self.hidden_dim_2 * 2,
                              num_layers=self.num_layers,
                              dropout=0.5, batch_first=True, bidirectional=True)
        self.SELayer20 = SELayer(128)
        self.fc20 = nn.Sequential(
            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.Tanh(),
            nn.Dropout(0.5),
        )
        self.SELayer21 = SELayer(64)
        self.fc21 = nn.Sequential(
            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.Tanh(),
            nn.Dropout(0.5),
            nn.Linear(32, 1)
        )

        self.lstm30 = nn.LSTM(input_size=self.input_features_2, hidden_size=self.hidden_dim_2,
                              num_layers=self.num_layers,
                              dropout=0.5, batch_first=True, bidirectional=True)
        self.lstm31 = nn.LSTM(input_size=self.hidden_dim_2 * 2, hidden_size=self.hidden_dim_2 * 2,
                              num_layers=self.num_layers,
                              dropout=0.5, batch_first=True, bidirectional=True)
        self.SELayer30 = SELayer(128)
        self.fc30 = nn.Sequential(
            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.Tanh(),
            nn.Dropout(0.5),
        )
        self.SELayer31 = SELayer(64)
        self.fc31 = nn.Sequential(
            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.Tanh(),
            nn.Dropout(0.5),
            nn.Linear(32, 1)
        )


        self.SELayer4 = SELayer(1152)
        self.fc4 = nn.Sequential(
            nn.Linear(1152, 512),
            nn.BatchNorm1d(512),
            nn.Tanh(),
            nn.Dropout(0.5))
        self.SELayer5 = SELayer(512)
        self.fc5 = nn.Sequential(
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.Tanh(),
            nn.Dropout(0.5))

        self.SELayer6 = SELayer(256)
        self.fc6 = nn.Sequential(nn.Linear(256, 1))

        for m in self.modules():
            if isinstance(m, nn.BatchNorm1d):
                m.weight.data.fill_(1)
                if m.bias is not None:
                    m.bias.data.fill_(0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight.data, 0, 0.01)
                if m.bias is not None:
                    m.bias.data.fill_(0)

    def forward(self, x0, x1, x2, x3):
        x00, (_, _) = self.lstm00(x0)
        x00, (_, _) = self.lstm01(x00)
        x00 = self.SELayer00(x00)
        x00 = x00.reshape(-1, 1024)
        x00 = self.fc00(x00)
        out0 = torch.unsqueeze(x00, 0)
        out0 = self.SELayer01(out0)
        out0 = out0.reshape(-1, 512)
        out0 = self.fc01(out0)

        x10, (_, _) = self.lstm10(x1)
        x10, (_, _) = self.lstm11(x10)
        x10 = self.SELayer10(x10)
        x10 = x10.reshape(-1, 1024)
        x10 = self.fc10(x10)
        out1 = torch.unsqueeze(x10, 0)
        out1 = self.SELayer11(out1)
        out1 = out1.reshape(-1, 512)
        out1 = self.fc11(out1)

        x20, (_, _) = self.lstm20(x2)
        x20, (_, _) = self.lstm21(x20)
        x20 = self.SELayer20(x20)
        x20 = x20.reshape(-1, 128)
        x20 = self.fc20(x20)
        out2 = torch.unsqueeze(x20, 0)
        out2 = self.SELayer21(out2)
        out2 = out2.reshape(-1, 64)
        out2 = self.fc21(out2)

        x30, (_, _) = self.lstm30(x3)
        x30, (_, _) = self.lstm31(x30)
        x30 = self.SELayer30(x30)
        x30 = x30.reshape(-1, 128)
        x30 = self.fc30(x30)
        out3 = torch.unsqueeze(x30, 0)
        out3 = self.SELayer31(out3)
        out3 = out3.reshape(-1, 64)
        out3 = self.fc31(out3)

        x = torch.cat((x00, x10), 1)
        x = torch.cat((x, x20), 1)
        x = torch.cat((x, x30), 1)

        x = torch.unsqueeze(x, 0)
        x = self.SELayer4(x)
        x = x.reshape(-1, 1152)
        x = self.fc4(x)

        x = torch.unsqueeze(x, 0)
        x = self.SELayer5(x)
        x = x.reshape(-1, 512)
        x = self.fc5(x)

        x = torch.unsqueeze(x, 0)
        x = self.SELayer6(x)
        x = x.reshape(-1, 256)
        x = self.fc6(x)
        return out0, out1, out2, out3, x


def LSTMMergeSENet():
    model = LSTMMergeSE()
    return model
