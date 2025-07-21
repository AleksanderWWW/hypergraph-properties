# === Load required libraries ===
library(ggplot2)     # For plotting
library(ggrepel)     # For non-overlapping text labels
library(ggpmisc)     # For regression formula annotation (optional)
library(readr)       # For reading CSV files

# === Read and prepare data ===

# Load correlation summary data
data <- read_csv("data/relationship_summary3.csv")

# Clean 'Hypergraph' column to use as label (strip prefixes/suffixes)
data$Label <- gsub("assortativity_|\\.csv", "", data$Hypergraph)

# Identify cases where Spearman and Pearson differ in sign
# Specifically: Pearson < 0 and Spearman > 0
data$LabelToShow <- ifelse(data$Pearson < 0 & data$Spearman > 0, data$Label, NA)

# Define regression formula for lm (used by geom_smooth)
formula <- y ~ x

# === Create scatter plot ===

p <- ggplot(data, aes(x = Pearson, y = Spearman)) +
  # Plot points
  geom_point() +
  # Add best-fit linear regression line (no confidence interval shading)
  geom_smooth(method = "lm", se = FALSE, color = "blue", formula = formula) +
  # Annotate selected points where signs differ
  geom_text_repel(aes(label = LabelToShow), na.rm = TRUE) +
  # Add dashed vertical and horizontal lines at zero
  geom_vline(xintercept = 0, linetype = "dashed", color = "gray50") +
  geom_hline(yintercept = 0, linetype = "dashed", color = "gray50") +
  # Add diagonal line y = x for visual reference
  geom_abline(slope = 1, intercept = 0, linetype = "dotted", color = "red") +
  # Minimal theme
  theme_minimal() +
  # Titles and axis labels
  labs(
    title = "Despite Overall Similarity, Spearman and Pearson Correlations\nDiffer in Sign for 17% of Hypergraphs (6/36)",
    x = "Pearson Correlation",
    y = "Spearman Correlation"
  )

# === Output and save ===

# Display the plot
print(p)

# Save as PDF and PNG (7x7 inches, high resolution)
ggsave("plots/pearson_vs_spearman.pdf", plot = p, width = 7, height = 7)
ggsave("plots/pearson_vs_spearman.png", plot = p, width = 7, height = 7, dpi = 300)
