# -------------------------------
# Setup: Total number of hypergraphs
# -------------------------------
N = 36  # Total sample size (e.g., number of hypergraphs)

# -------------------------------
# 1. Analysis for "No-relationship" category
# -------------------------------
n = 3  # Number of hypergraphs classified as "No relationship"

# Proportion estimate (frequentist)
n / N * 100  # Simple proportion as percentage

# Bayesian posterior mean estimate with uniform Beta(1,1) prior
(n + 1) / (N + 2) * 100  # Posterior mean in Bayesian beta-binomial model

# Posterior distribution for this category
curve(dbeta(x, shape1 = n + 1, shape2 = N - n + 1),
      main = "Posterior PDF for 'No-relationship'", ylab = "Density")

# Posterior CDF (cumulative distribution)
curve(pbeta(x, shape1 = n + 1, shape2 = N - n + 1),
      main = "Posterior CDF for 'No-relationship'", ylab = "Cumulative probability")

# 99% Bayesian prediction interval
qbeta(0.005, shape1 = n + 1, shape2 = N - n + 1) * 100  # Lower bound
qbeta(0.995, shape1 = n + 1, shape2 = N - n + 1) * 100  # Upper bound

# 95% Bayesian prediction interval
qbeta(0.025, shape1 = n + 1, shape2 = N - n + 1) * 100  # Lower bound
qbeta(0.975, shape1 = n + 1, shape2 = N - n + 1) * 100  # Upper bound

# -------------------------------
# 2. Analysis for "Complex relationship" category
# -------------------------------
n = 15  # Number of hypergraphs with complex (non-monotonic) relationship

# Proportion estimate (frequentist)
n / N * 100  # As percentage

# Bayesian posterior mean with Beta(1,1) prior
(n + 1) / (N + 2) * 100

# Posterior PDF
curve(dbeta(x, shape1 = n + 1, shape2 = N - n + 1),
      main = "Posterior PDF for 'Complex-relationship'", ylab = "Density")

# Posterior CDF
curve(pbeta(x, shape1 = n + 1, shape2 = N - n + 1),
      main = "Posterior CDF for 'Complex-relationship'", ylab = "Cumulative probability")

# 99% prediction interval
qbeta(0.005, shape1 = n + 1, shape2 = N - n + 1) * 100  # Lower bound
qbeta(0.995, shape1 = n + 1, shape2 = N - n + 1) * 100  # Upper bound

# 95% prediction interval
qbeta(0.025, shape1 = n + 1, shape2 = N - n + 1) * 100  # Lower bound
qbeta(0.975, shape1 = n + 1, shape2 = N - n + 1) * 100  # Upper bound
