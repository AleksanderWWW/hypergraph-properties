# Load required libraries
library(dplyr)
library(glue)

# === Load and pre-process the first dataset (relationship summary) ===

# Read CSV with summary data
st = read.csv("data/relationship_summary3_direction.csv")

# Set alpha threshold for significance
alfa = 0.00001

# Add human-readable label for monotonicity classification
st$increasing2 = ifelse(st$Description == "No relationship", "Non-sign.", st$increasing)

# Classify Pearson correlation direction only if statistically significant
st$PearsonPositiv = ifelse(st$Linear.F.test > alfa, "Non-sign.", st$Pearson > 0)

# Remove three outlier rows and drop selected columns to simplify the dataset
st2 = st[-c(3, 23, 33), -c(2:6, 11)]

# Check cleaned column names
names(st2)

# Tabulate how Pearson sign aligns with monotonicity direction
table(st2$PearsonPositiv, st2$increasing2)

# Clean hypergraph names
st2$Hypergraph = gsub("assortativity_|\\.csv", "", st2$Hypergraph)

# === Load and pre-process the second dataset (correlation p-values) ===

# Read correlation results and subset columns (keep name + p-values for 3 methods)
pvals = read.csv("data/corr_result_1750858355_9527603.csv")
pvals = pvals[-c(1:10), c(1, 26:31)]

# Merge cleaned summary data (st2) with p-value data
merged_df <- merge(st2, pvals, by.x = "Hypergraph", by.y = "name", all.x = TRUE)

# Determine direction of Spearman and Kendall only if significant (based on p-value)
merged_df$SpearmanPositiv = ifelse(merged_df$assortativity_spearmanr_pvalue > alfa, "Non-sign.", merged_df$Spearman > 0)
merged_df$KendallPositiv  = ifelse(merged_df$assortativity_kendalltau_pvalue > alfa, "Non-sign.", merged_df$Kendall > 0)

# Cross-tabulate directionality vs. monotonicity for all three correlation types
table(st2$PearsonPositiv,  st2$increasing2)
table(merged_df$SpearmanPositiv, merged_df$increasing2)
table(merged_df$KendallPositiv,  merged_df$increasing2)

# Check intermediate columns (debug/inspect)
merged_df[, c(1:4, 6, 9, 11, 13)]

# === Reformat merged data ===

# Remove original correlation columns before renaming
merged_df$Pearson = merged_df$Spearman = merged_df$Kendall = NULL

# Rename new correlation columns to standard names
names(merged_df)[c(5, 7, 9)] = c("Pearson", "Spearman", "Kendall")

# Keep final subset of columns for table generation
df = merged_df[, c(1, 3, 5:10)]

# === Define helper functions for LaTeX table formatting ===

# Function to convert p-values into significance stars
star <- function(p) {
  if      (p < 1e-5)  return("***")
  else if (p < 1e-2)  return("**")
  else if (p < 5e-2)  return("*")
  else                return("")
}

# Function to convert logical direction into label
abbr <- function(x) {
  if      (x == "TRUE")      "Inc"
  else if (x == "FALSE")     "Dec"
  else                       "Non-sign."
}

# === Create LaTeX table rows with correlation + significance + monotonicity ===

df %>%
  # Add significance stars and monotonicity abbreviation
  mutate(
    s_pear = sapply(assortativity_pearsonr_pvalue, star),
    s_spear = sapply(assortativity_spearmanr_pvalue, star),
    s_kend = sapply(assortativity_kendalltau_pvalue, star),
    inc2 = sapply(increasing2, abbr)
  ) %>%
  # Format correlation values to 3 decimals
  mutate_at(vars(Pearson, Spearman, Kendall), ~ sprintf("%.3f", .)) %>%
  # Sort by decreasing Pearson
  arrange(desc(as.numeric(Pearson))) %>%
  # Compose LaTeX row strings
  transmute(
    row = glue(
      "{Hypergraph} & ",
      "{Pearson}{s_pear} & ",
      "{Spearman}{s_spear} & ",
      "{Kendall}{s_kend} & ",
      "{inc2} \\\\"
    )
  ) -> rows

# === Output full LaTeX table ===

cat("\\begin{table}[ht]\n",
    "  \\centering\n",
    "  \\begin{tabular}{lcccc}\n",
    "    \\toprule\n",
    "    Hypergraph & Pearson & Spearman & Kendall & Monotonicity\\\\\n",
    "    \\midrule\n",
    paste0("    ", rows$row, collapse = "\n"),
    "\n    \\bottomrule\n",
    "  \\end{tabular}\n",
    "  \\caption{Correlation measures (sorted by decreasing Pearson) ",
    "with significance stars (* $p<0.05$, ** $p<0.01$, *** $p<0.00001$).}\n",
    "  \\label{tab:hypergraph_assortativity}\n",
    "\\end{table}\n",
    sep = "")
