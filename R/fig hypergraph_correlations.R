library(readr)
library(dplyr)
library(tidyr)
library(ggplot2)
library(forcats)

# 1. Read and parse the data
df <- read_tsv("data/nodeEdgeBipartite.csv", col_types = cols(
  `Hipergraph name` = col_character(),
  `Node-centric`    = col_character(),
  `Edge-centric`    = col_character(),
  `Degree-degree`         = col_character()
)) %>%
  # 2. strip "%" and convert to numeric proportions
  mutate(across(-`Hipergraph name`, ~ parse_number(.) / 100)) %>%
  rename(Hypergraph = `Hipergraph name`) %>%
  # 3. reorder Hypergraph factor by descending Bipartite
  arrange(`Degree-degree`) %>%
  mutate(Hypergraph = fct_inorder(Hypergraph))

# 4. Pivot to long format **including** Bipartite
df_long <- df %>%
  pivot_longer(-Hypergraph,
               names_to  = "Correlation_Type",
               values_to = "Value")

# 5. Plot: clustered bars, horizontal orientation, sorted by Bipartite
p<-ggplot(df_long, aes(x = Hypergraph, y = Value, fill = Correlation_Type)) +
  geom_col(position = position_dodge(width = 0.8), width = 0.7) +
  coord_flip() +
  scale_y_continuous(
    labels = scales::percent_format(accuracy = 1),
    limits = c(-0.5, 1.0),    # –50% to 100%
    expand = c(.01, .01)         # no extra padding
  ) +
  labs(
    #title = "Degree–Degree Correlations by Hypergraph (sorted by Bipartite)",
    x     = NULL,
    y     = "Pearson correlation between hyperedge size and degree",
    fill  = "Pre-processed data:"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    axis.text.y = element_text(size = 8),
    legend.position = "top"
  )

print(p)
# Save as PDF, 8" wide by 10" tall:
ggsave("hypergraph_correlations.pdf", plot = p,
       width = 8, height = 10, units = "in")
