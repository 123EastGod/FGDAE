import torch.nn as nn
import torch


def LinearBnRelu(input_dim, out_dim):
    linear_bn_relu = nn.Sequential(
        nn.Linear(input_dim, out_dim), nn.BatchNorm1d(out_dim), nn.ReLU(inplace=True))
    return linear_bn_relu


class VAE(nn.Module):
    ''' Vanilla AE '''
    def __init__(self, input_dim):
        super(VAE, self).__init__()

        self.encoder = nn.Sequential(
            LinearBnRelu(input_dim, 64),
            nn.Linear(64, 16))

        self.mean = nn.Linear(16, 16)
        self.logstd = nn.Linear(16, 16)

        self.decoder = nn.Sequential(
            LinearBnRelu(16, 64),
            nn.Linear(64, input_dim))

    def forward(self, x, mode):
        z = self.encoder(x)
        z_mean = self.mean(z)
        z_logstd = self.logstd(z)
        noise = torch.randn(z.shape).cuda()
        z = noise * torch.exp(z_logstd) + z_mean
        output = self.decoder(z)

        return output, z