import yaml
import numpy as np
import torch
import torch.optim as optim
import json
import time
from collections import deque
from data_ingestor import DataIngestor
from pattern_encoder import PatternEncoder
from forecast_generator import ForecastGenerator
from meta_loss import compute_meta_loss
from orchestrator import Orchestrator

forecast_entropy_window = deque(maxlen=100)

def log_forecast_entropy(S, path="logs/forecast_entropy.jsonl"):
    try:
        flat = S.detach().cpu().numpy().flatten()
        hist, _ = np.histogram(flat, bins=20, density=True)
        hist = hist[hist > 0]
        entropy = -np.sum(hist * np.log2(hist))
        forecast_entropy_window.append(entropy)
        delta_H = 0 if len(forecast_entropy_window) < 2 else entropy - forecast_entropy_window[-2]
        beacon = {
            "t": time.time(),
            "H": entropy,
            "delta_H": delta_H
        }
        with open(path, "a") as f:
            f.write(json.dumps(beacon) + "\n")
        print("[FORECAST ENTROPY] Logged:", beacon)
    except Exception as e:
        print("[FORECAST ENTROPY ERROR]", e)

def train_one_epoch(encoder, forecaster, optimizer, batch_data, config, device):
    encoder.train()
    forecaster.train()
    seq_len = config["model"]["forecast_steps"] + 1
    x_input = batch_data[:, 0, :].astype(np.float32)
    x_target = batch_data[:, 1:seq_len, :].astype(np.float32)
    x_input_tensor = torch.from_numpy(x_input).to(device)
    x_target_tensor = torch.from_numpy(x_target).to(device)
    z = encoder(x_input_tensor)
    S = forecaster(z)
    resource_cost = torch.tensor(0.0).to(device)
    synergy_score = torch.tensor(0.0).to(device)
    loss = compute_meta_loss(S, x_target_tensor, config, resource_cost, synergy_score)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss.item(), S, x_target_tensor

def main():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    ingestor = DataIngestor(config)
    input_dim = config["model"]["input_dim"]
    latent_dim = config["model"]["latent_dim"]
    forecast_steps = config["model"]["forecast_steps"]
    hidden_dim = config["model"]["hidden_dim"]
    learning_rate = config["model"]["learning_rate"]
    encoder = PatternEncoder(input_dim, latent_dim, hidden_dim).to(device)
    forecaster = ForecastGenerator(latent_dim, input_dim, forecast_steps, hidden_dim).to(device)
    params = list(encoder.parameters()) + list(forecaster.parameters())
    optimizer = optim.Adam(params, lr=learning_rate)
    max_epochs = config["training"]["max_epochs"]
    batch_size = config["training"]["batch_size"]
    orchestrator = Orchestrator(config)
    print("Starting Training...")
    for epoch in range(max_epochs):
        historical_data = ingestor.get_historical_batch(length=64)
        batch_samples = []
        for _ in range(batch_size):
            if len(historical_data) < (forecast_steps + 1):
                continue
            idx = np.random.randint(0, len(historical_data) - (forecast_steps + 1))
            sample = historical_data[idx: idx + (forecast_steps + 1)]
            batch_samples.append(sample)
        batch_samples = np.array(batch_samples)
        loss_value, S, X_target = train_one_epoch(encoder, forecaster, optimizer, batch_samples, config, device)
        log_forecast_entropy(S)
        if (epoch + 1) % 5 == 0:
            print(f"Epoch {epoch + 1}/{max_epochs} | Loss: {loss_value:.4f}")
        system_state = {
            "recent_errors": [loss_value, loss_value*1.01, loss_value*0.99],
            "recent_configs": [[config["model"]["learning_rate"]]]*3,
            "error_streak": 3,
            "entropy_spike": (epoch % 10 == 0),
            "domain_shift": False
        }
        orchestrator.step(system_state)
    print("Training Complete.")
    encoder.eval()
    forecaster.eval()
    current_state = ingestor.get_next()
    current_state_tensor = torch.from_numpy(current_state.astype(np.float32)).unsqueeze(0).to(device)
    with torch.no_grad():
        z = encoder(current_state_tensor)
        prediction = forecaster(z)
    print("Current State:")
    print(current_state)
    print("Predicted next steps:")
    print(prediction.cpu().numpy())

if __name__ == "__main__":
    main()
