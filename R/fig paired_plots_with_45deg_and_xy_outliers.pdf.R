library(dplyr)
library(tidyr)
library(ggplot2)
library(scales)
library(ggpubr)
library(ggrepel)
library(patchwork)

# assume df_long exists; pivot to wide
df_wide <- df_long %>%
  pivot_wider(names_from = Correlation_Type, values_from = Value)

# helper: pick top-n by absolute difference x-y
get_outliers_xy <- function(df, xvar, yvar, n = 4) {
  df %>%
    mutate(diff = abs(.data[[xvar]] - .data[[yvar]])) %>%
    slice_max(order_by = diff, n = n) %>%
    pull(Hypergraph)
}

# compute top-4 abs(X-Y) for each pair
out12 <- get_outliers_xy(df_wide, "Node-centric", "Edge-centric")
out13 <- get_outliers_xy(df_wide, "Node-centric", "Degree-degree")
out23 <- get_outliers_xy(df_wide, "Edge-centric", "Degree-degree")

# common theme
common_theme <- theme_minimal(base_size = 12) +
  theme(
    legend.position = "none",
    axis.text  = element_text(size = 9),
    axis.title = element_text(size = 11)
  )

# text‐repel settings
repel_args <- list(
  segment.size  = 0.3,
  segment.color = "grey50",
  arrow         = arrow(length = unit(0.01, "npc")),
  box.padding   = 0.3,
  max.overlaps  = 20,
  force         = 1
)

# 1: Node-centric vs Edge-centric
p1 <- ggplot(df_wide, aes(x = `Node-centric`, y = `Edge-centric`)) +
  geom_abline(slope = 1, intercept = 0, linetype = "dotted") +
  geom_vline(xintercept = 0, linetype = "dashed") +
  geom_hline(yintercept = 0, linetype = "dashed") +
  geom_point(alpha = 0.7) +
  geom_smooth(method = "lm", se = FALSE, color = "black") +
  stat_regline_equation(
    aes(label = paste(..eq.label.., ..rr.label.., sep = "~~~")),
    formula = y ~ x, label.x = 0.255, label.y = -0.45
  ) +
  geom_text_repel(
    data = filter(df_wide, Hypergraph %in% out12),
    aes(label = Hypergraph),
    segment.size  = repel_args$segment.size,
    segment.color = repel_args$segment.color,
    arrow         = repel_args$arrow,
    box.padding   = repel_args$box.padding,
    max.overlaps  = repel_args$max.overlaps,
    force         = repel_args$force
  ) +
  scale_x_continuous(labels = percent_format(1), limits = c(-0.5, 1.0)) +
  scale_y_continuous(labels = percent_format(1), limits = c(-0.5, .5)) +
  labs(x = "Node-centric Pearson correlation", y = "Edge-centric Pearson correlation",
       title="(c) Node-centric vs Edge-centric") +
  common_theme

# 2: Node-centric vs Degree-degree
p2 <- ggplot(df_wide, aes(x = `Node-centric`, y = `Degree-degree`)) +
  geom_abline(slope = 1, intercept = 0, linetype = "dotted") +
  geom_vline(xintercept = 0, linetype = "dashed") +
  geom_hline(yintercept = 0, linetype = "dashed") +
  geom_point(alpha = 0.7) +
  geom_smooth(method = "lm", se = FALSE, color = "black") +
  stat_regline_equation(
    aes(label = paste(..eq.label.., ..rr.label.., sep = "~~~")),
    formula = y ~ x, label.x = 0.255, label.y = -0.45
  ) +
  geom_text_repel(
    data = filter(df_wide, Hypergraph %in% out13),
    aes(label = Hypergraph),
    segment.size  = repel_args$segment.size,
    segment.color = repel_args$segment.color,
    arrow         = repel_args$arrow,
    box.padding   = repel_args$box.padding,
    max.overlaps  = repel_args$max.overlaps,
    force         = repel_args$force
  ) +
  scale_x_continuous(labels = percent_format(1), limits = c(-0.5, 1.0)) +
  scale_y_continuous(labels = percent_format(1), limits = c(-0.5, .5)) +
  labs(x = "Node-centric Pearson correlation", y = "Bipartite Pearson correlation",
       title="(b) Bipartite vs Node-centric") +
  common_theme

# 3: Edge-centric vs Degree-degree
p3 <- ggplot(df_wide, aes(x = `Edge-centric`, y = `Degree-degree`)) +
  geom_abline(slope = 1, intercept = 0, linetype = "dotted") +
  geom_vline(xintercept = 0, linetype = "dashed") +
  geom_hline(yintercept = 0, linetype = "dashed") +
  geom_point(alpha = 0.7) +
  geom_smooth(method = "lm", se = FALSE, color = "black") +
  stat_regline_equation(
    aes(label = paste(..eq.label.., ..rr.label.., sep = "~~~")),
    formula = y ~ x, label.x = 0.255, label.y = -0.45
  ) +
  geom_text_repel(
    data = filter(df_wide, Hypergraph %in% out23),
    aes(label = Hypergraph),
    segment.size  = repel_args$segment.size,
    segment.color = repel_args$segment.color,
    arrow         = repel_args$arrow,
    box.padding   = repel_args$box.padding,
    max.overlaps  = repel_args$max.overlaps,
    force         = repel_args$force
  ) +
  scale_x_continuous(labels = percent_format(1), limits = c(-0.5, 1)) +
  scale_y_continuous(labels = percent_format(1), limits = c(-0.5, .5)) +
  labs(x = "Edge-centric Pearson correlation", y = "Bipartite Pearson correlation",
       title="(a) Bipartite vs Edge-centric") +
  common_theme

# 4: density panel as before
p4 <- ggplot(df_long, aes(x = Value, fill = Correlation_Type)) +
  geom_density(alpha = 0.5, size = 0.3) +
  scale_x_continuous(labels = percent_format(1), limits = c(-0.5, 1.0)) +
  labs(
    x = "Pearson correlation",
    y = "Density",
    fill = "Pre-processed step:",
    title = "(d) Distributions of Correlations"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    legend.position   = c(0.75, 0.75),
    legend.background = element_rect(fill = alpha("white", 0.7), color = NA),
    axis.text  = element_text(size = 9),
    axis.title = element_text(size = 11)
  )

# assemble 2×2
layout <- (p3 | p2) /
  (p1 | p4)

print(layout)
ggsave("paired_plots_with_45deg_and_xy_outliers.pdf", layout, width = 12, height = 10)


df_wide_ordered <- df_wide %>%
  mutate(diff_node_degree = abs(`Node-centric` - `Edge-centric`)) %>%
  arrange(desc(diff_node_degree))

print(df_wide_ordered, n = 9999)
