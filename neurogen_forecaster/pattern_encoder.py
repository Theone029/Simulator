import torch
import torch.nn as nn

class PatternEncoder(nn.Module):
    """
    A simple MLP encoder to transform the input state x(t) into a latent vector P(t).
    """
    def __init__(self, input_dim, latent_dim, hidden_dim=64):
        super(PatternEncoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, latent_dim)
        )

    def forward(self, x):
        # x: Tensor of shape (batch_size, input_dim)
        return self.encoder(x)
