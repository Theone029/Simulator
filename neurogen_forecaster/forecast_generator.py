import torch
import torch.nn as nn

class ForecastGenerator(nn.Module):
    """
    Multi-step forecaster: generates K future state predictions from the latent vector.
    Each future step prediction is produced by its own MLP head.
    """
    def __init__(self, latent_dim, output_dim, forecast_steps, hidden_dim=64):
        super(ForecastGenerator, self).__init__()
        self.forecast_steps = forecast_steps
        self.heads = nn.ModuleList([
            nn.Sequential(
                nn.Linear(latent_dim, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, output_dim)
            ) for _ in range(forecast_steps)
        ])

    def forward(self, z):
        # z: Tensor of shape (batch_size, latent_dim)
        predictions = []
        for head in self.heads:
            pred = head(z)  # shape: (batch_size, output_dim)
            predictions.append(pred.unsqueeze(1))
        # Concatenate predictions to shape: (batch_size, forecast_steps, output_dim)
        return torch.cat(predictions, dim=1)
