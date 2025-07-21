# ---------------------------------------
# Load required package (with install fallback)
# ---------------------------------------
if (!require(lsr)) install.packages("lsr", dependencies = TRUE)
library(lsr)

# ---------------------------------------
# Load and preprocess data
# ---------------------------------------
# Read tab-separated file containing hypergraph statistics
data <- read.table("data/eta.txt", sep = "\t", header = TRUE, dec = ".")

# Exclude synthetic datasets (like ABCD) from analysis
data <- data[!grepl("ABCD", data$Hypergraph), ]

# ---------------------------------------
# Set up variables
# ---------------------------------------
# Extract categorical variable (semantic category of hypergraphs)
category_var <- as.factor(data[[2]])

# Identify columns with continuous variables (eta² target)
continuous_vars <- names(data)[3:11]

# ---------------------------------------
# Function to compute eta² for each variable
# ---------------------------------------
get_eta <- function(var_name) {
  etaSquared(aov(data[[var_name]] ~ category_var))[[1]]
}

# Apply eta² computation to each continuous variable
eta_values <- sapply(continuous_vars, get_eta)
names(eta_values) <- continuous_vars

# ---------------------------------------
# Parse variable names into row/column parts
# ---------------------------------------
# E.g., "node_Pearson" → row = "node", column = "Pearson"
var_parts <- do.call(rbind, strsplit(continuous_vars, "_"))
row_names <- var_parts[,1]
col_names <- var_parts[,2]

# ---------------------------------------
# Store results in 3×3 matrix
# ---------------------------------------
eta_matrix <- matrix(NA, nrow = 3, ncol = 3,
                     dimnames = list(c("node", "edge", "bi"),
                                     c("Pearson", "Spearman", "Kendall")))

# Fill the matrix using parsed names
for (i in seq_along(eta_values)) {
  r <- row_names[i]
  c <- col_names[i]
  eta_matrix[r, c] <- eta_values[i]
}

# Print matrix to console
print(eta_matrix)

# ---------------------------------------
# Generate LaTeX tabular output
# ---------------------------------------
latex_table <- "\\begin{tabular}{lccc}
\\toprule
 & Pearson & Spearman & Kendall \\\\\n\\midrule\n"

for (r in rownames(eta_matrix)) {
  row_vals <- sprintf("%.4f", eta_matrix[r, ])  # format to 4 decimal places
  latex_table <- paste0(latex_table, r, " & ",
                        paste(row_vals, collapse = " & "), " \\\\\n")
}

latex_table <- paste0(latex_table, "\\bottomrule\n\\end{tabular}")

# Output the LaTeX-formatted table to console
cat(latex_table)
