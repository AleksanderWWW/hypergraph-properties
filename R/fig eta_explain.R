# ========================================================
# Libraries
# ========================================================
library(lsr)         # For effect size measures like eta squared
library(ggpubr)      # For publication-ready ggplot themes
library(dplyr)       # Data manipulation
library(ggplot2)     # Visualization
library(forcats)     # Factor reordering
library(tidyr)       # Pivoting
library(stringr)     # String operations

# ========================================================
# Load and preprocess data
# ========================================================
data <- read.table("data/eta.txt", sep = "\t", header = TRUE, dec = ".")

# Extract category label (column 2) and store as factor
category_var <- as.factor(data[[2]])

# Identify continuous correlation columns (node/edge/bi × correlation type)
continuous_vars <- names(data)[3:11]

# ========================================================
# Long format transformation
# ========================================================
df_long <- data %>%
  pivot_longer(
    cols = c(node_Pearson, node_Spearman, edge_Pearson, edge_Spearman, 
             edge_Kendall, node_Kendall, bi_Pearson, bi_Spearman, bi_Kendall),
    names_to = "variable", values_to = "value"
  )

# ========================================================
# Clean & filter data
# ========================================================

# Remove specific categories
df_long <- df_long %>%
  filter(Category != "product-category") %>%
  filter(Category != "ABCD-h")

# Format category labels: Title case + fix 'And'
df_long <- df_long %>%
  mutate(
    Category = str_to_title(Category),
    Category = str_replace(Category, "\\bAnd\\b", "and")
  )

# Filter only Pearson and Spearman metrics (ignore Kendall for now)
df_long <- df_long %>%
  filter(variable %in% c("node_Pearson", "node_Spearman",
                         "edge_Pearson", "edge_Spearman", 
                         "bi_Pearson", "bi_Spearman"))

# Improve axis readability by breaking variable names
df_long$variable <- gsub("_", "\n", df_long$variable)

# ========================================================
# Main Boxplot Visualization: Correlation by Method & Category
# ========================================================
p <- ggplot(df_long, aes(x = variable, y = value, fill = variable)) +
  geom_boxplot(outlier.shape = NA, alpha = 0.7) +  # Remove outlier dots
  geom_jitter(width = 0.2, alpha = 0.3, size = 0.8) +
  facet_wrap(~ Category, scales = "free_y", ncol = 3, nrow = 4) +
  labs(
    title = "Bipartite Representation Minimizes Correlation Variance Within Categories",
    x = "Data Pre-processing and correlation coefficient",
    y = "Correlation coefficient value"
  ) +
  theme_pubr() +
  theme(
    legend.position = "none",
    strip.text = element_text(size = 12, face = "bold")
  ) +
  ylim(-0.6, 0.9)  # Manually clip y-axis

# Output and save
print(p)
ggsave(
  filename = file.path("plots", "eta_explain.pdf"),
  plot = p,
  width = 15, height = 4/3 * 15
)
