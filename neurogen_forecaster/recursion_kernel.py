import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import zlib
import json

class SimpleEnv:
    def __init__(self, x0=0.0, noise_std=0.1):
        self.x = x0
        self.noise_std = noise_std

    def step(self, action):
        noise = np.random.randn() * self.noise_std
        self.x += action + noise
        return self.x, self.x**2

    def reset(self, x0=0.0):
        self.x = x0
        return self.x

def shannon_entropy(data, bins=20):
    if len(data) == 0:
        return 0.0
    hist, _ = np.histogram(data, bins=bins, density=True)
    hist = hist[hist > 0]
    return -np.sum(hist * np.log2(hist))

class EntropyMonitor:
    def __init__(self, window=1000):
        self.history = deque(maxlen=window)

    def update(self, value):
        self.history.append(value)

    def get_entropy(self):
        return shannon_entropy(np.array(self.history))

    def get_raw_log(self):
        return list(self.history)

    def compression_score(self):
        raw = json.dumps(self.get_raw_log()).encode('utf-8')
        compressed = zlib.compress(raw)
        return {
            'raw_bytes': len(raw),
            'compressed_bytes': len(compressed),
            'compression_ratio': len(compressed) / len(raw) if len(raw) > 0 else 1.0
        }

class SimpleController(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(1, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x):
        return self.net(x)

class RecursionKernel:
    def __init__(self, x0=2.0, noise_std=0.1, lr=1e-3):
        self.env = SimpleEnv(x0, noise_std)
        self.mu = SimpleController()
        self.optimizer = torch.optim.Adam(self.mu.parameters(), lr=lr)
        self.entropy_monitor = EntropyMonitor()
        self._last_entropy = None
        self.metrics = {}
        self.symbols = {
            'x_t': 'System state',
            'u_t': 'Control action',
            'C(t)': 'Cost (x²)',
            'H(x)': 'Entropy of recent x',
            'delta_H': 'Entropy delta',
            'mu': 'Controller',
            'optimizer': 'Optimizer'
        }

    def step(self):
        x = self.env.x
        x_tensor = torch.FloatTensor([[x]])
        u = self.mu(x_tensor).item()
        x_next, C = self.env.step(u)
        self.optimizer.zero_grad()
        torch.tensor(C, requires_grad=True).backward()
        self.optimizer.step()
        H_prev = self.entropy_monitor.get_entropy()
        self.entropy_monitor.update(x_next)
        H_now = self.entropy_monitor.get_entropy()
        delta_H = H_now - H_prev if H_prev is not None else 0.0
        compression = self.entropy_monitor.compression_score()
        self.metrics = {
            'x_t': x_next,
            'u_t': u,
            'C(t)': C,
            'H(x)': H_now,
            'delta_H': delta_H,
            'compression': compression
        }
        self._last_entropy = H_now
        return self.metrics

    def get_symbols(self, export=False):
        return json.dumps(self.symbols, indent=2) if export else self.symbols

    def get_metrics(self):
        return self.metrics

    def get_internal_refs(self):
        return {
            'mu': self.mu,
            'optimizer': self.optimizer,
            'entropy_monitor': self.entropy_monitor
        }

    def clone_with(self, x0=None, noise_std=None, lr=None):
        return RecursionKernel(
            x0 or self.env.x,
            noise_std or self.env.noise_std,
            lr or self.optimizer.param_groups[0]['lr']
        )

    def to_symbolic_tokens(self):
        return {
            'mu': str(self.mu),
            'optimizer': str(self.optimizer),
            'x_t': self.env.x,
            'H(x)': self.entropy_monitor.get_entropy(),
            'delta_H': self.metrics.get('delta_H', 0),
            'C(t)': self.metrics.get('C(t)', 0),
            'compression_ratio': self.metrics.get('compression', {}).get('compression_ratio', 1.0)
        }

def inject_kernel_symbols(kernel):
    tokens = kernel.to_symbolic_tokens()
    print("[SYMBOLS]", json.dumps(tokens, indent=2))
    return tokens
