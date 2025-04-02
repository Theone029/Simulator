import torch

def compute_meta_loss(S, X_target, config, resource_cost=0.0, synergy_score=0.0):
    """
    Compute the combined meta-error M(t) from:
      - Multi-step prediction error (MSE)
      - Distribution alignment (placeholder using L1 difference)
      - Resource usage penalty (resource_cost)
      - Synergy reward (synergy_score)

    Parameters:
      S: Predictions, Tensor of shape (batch_size, K, d)
      X_target: Ground truth for next K steps, Tensor of shape (batch_size, K, d)
      config: Configuration dictionary with meta parameters
      resource_cost: Scalar tensor for resource usage
      synergy_score: Scalar tensor for synergy (higher is better)

    Returns:
      M: Scalar meta-error tensor.
    """
    alpha_k = config["meta"]["alpha_k"]
    beta_k = config["meta"]["beta_k"]
    rho = config["meta"]["rho"]
    gamma = config["meta"]["gamma"]
    lamb = config["meta"]["lambda"]
    delta = config["meta"]["delta"]

    batch_size, K, d = S.shape

    # 1) Multi-step Prediction Error (using MSE)
    mse_loss = 0.0
    for k in range(K):
        diff = S[:, k, :] - X_target[:, k, :]
        mse_loss += alpha_k[k] * torch.mean(diff ** 2)

    # 2) Distribution Alignment Error (placeholder using L1 norm)
    dist_align = 0.0
    for k in range(K):
        diff = S[:, k, :] - X_target[:, k, :]
        dist_align += beta_k[k] * torch.mean(torch.abs(diff))

    # 3) Combine errors into the meta-loss.
    meta_loss = mse_loss + gamma * dist_align + lamb * resource_cost - delta * synergy_score

    return meta_loss
