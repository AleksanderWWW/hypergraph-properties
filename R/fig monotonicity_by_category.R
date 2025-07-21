# ========================================================
# Load Required Libraries
# ========================================================
library(lsr)        # For eta squared effect size
library(ggpubr)     # Publication-ready themes for ggplot2
library(dplyr)      # Data manipulation
library(ggplot2)    # Data visualization
library(forcats)    # Factor reordering
library(tidyr)      # Data reshaping
library(stringr)    # String operations

# ========================================================
# Load and Prepare Data
# ========================================================
data <- read.table("data/eta.txt", sep = "\t", header = TRUE, dec = ".")

# Extract category column (2nd col) as factor
category_var <- as.factor(data[[2]])

# List of continuous variable columns (Pearson, Spearman, Kendall by view)
continuous_vars <- names(data)[3:11]

# Reshape to long format for visualization
df_long <- data %>%
  pivot_longer(
    cols = c(node_Pearson, node_Spearman, edge_Pearson, edge_Spearman,
             edge_Kendall, node_Kendall, bi_Pearson, bi_Spearman, bi_Kendall),
    names_to = "variable", values_to = "value"
  )

# Optional filter — keep if re-adding: exclude "product-category"
# df_long <- df_long %>% filter(Category != "product-category")

# Remove ABCD-h synthetic benchmark
df_long <- df_long %>%
  filter(Category != "ABCD-h")

# Clean category labels: capitalize and replace 'And' properly
df_long <- df_long %>%
  mutate(
    Category = str_to_title(Category),
    Category = str_replace(Category, "\\bAnd\\b", "and")
  )

# Filter only node/edge/bipartite with Pearson and Spearman (exclude Kendall)
df_long <- df_long %>%
  filter(variable %in% c("node_Pearson", "node_Spearman",
                         "edge_Pearson", "edge_Spearman",
                         "bi_Pearson", "bi_Spearman"))

# Format variable labels for axis (e.g., 'node_Pearson' → 'node\nPearson')
df_long$variable <- gsub("_", "\n", df_long$variable)

# ========================================================
# Analyze Sign Direction of Bi-Pearson Correlation
# ========================================================
dflong2 <- df_long %>%
  filter(variable == "bi\nPearson") %>%
  mutate(sign = if_else(value > 0, "Positive", "Negative")) %>%
  mutate(
    # Manual override for certain hypergraphs
    sign = if_else(
      Hypergraph %in% c("vegas-bars-reviews", "amazon", "InVS13"),
      "Non-sign.",
      if_else(
        Hypergraph %in% c("email-enron"),
        "Positive",
        sign
      )
    )
  )

# ========================================================
# Create Bar Plot of Sign Distributions by Category
# ========================================================
p_sign <- dflong2 %>%
  mutate(Category = fct_rev(fct_infreq(Category))) %>%  # Order by frequency
  ggplot(aes(x = Category, fill = sign)) +
  geom_bar() +
  coord_flip() +  # Flip for better readability
  labs(
    x = "Hypergraph Category",
    y = "Count of Empirical Hypergraphs",
    fill = "Monotonicity",
    title = "Monotonic Trend Direction by Hypergraph Category"
  ) +
  scale_fill_manual(
    values = c(
      "Positive" = "#1b9e77",
      "Negative" = "#d95f02",
      "Non-sign." = "#7570b3"
    ),
    labels = c(
      "Positive" = "Inc.",
      "Negative" = "Dec.",
      "Non-sign." = "Non-sign."
    )
  ) +
  theme_minimal(base_size = 12) +
  theme(
    axis.text.y = element_text(size = 10)  # y-axis now shows categories
  )

# Print the plot to viewer
print(p_sign)

# Save the plot to file
ggsave(
  filename = "plots/monotonicity_by_category.pdf",
  plot = p_sign,
  width = 8,
  height = 6,
  units = "in"  # inches; use cairo for sharp PDF output if needed
)
