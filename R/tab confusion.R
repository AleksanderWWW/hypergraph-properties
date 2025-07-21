# ========================================================
# Load Required Package
# ========================================================
# Install and load xtable (used to create LaTeX tables)
if (!require("xtable")) install.packages("xtable", dependencies = TRUE)
library(xtable)

# ========================================================
# Load Original and Switched Direction Datasets
# ========================================================
# Read original and direction-switched classification summaries
df_switched <- read.csv("data/relationship_summary_switched.csv", stringsAsFactors = FALSE)
df_original <- read.csv("data/relationship_summary3.csv", stringsAsFactors = FALSE)

# ========================================================
# Prepare Labels for Consistent Category Ordering
# ========================================================
# Define the relationship levels in the desired logical order
relationship_levels <- c("No relationship", "Linear", "Monotonic", "Non-monotonic")

# Convert 'Description' columns to factors using this order
desc_switched <- factor(df_switched$Description, levels = relationship_levels)
desc_original <- factor(df_original$Description, levels = relationship_levels)

# ========================================================
# Build Confusion Matrix
# ========================================================
# Create contingency table comparing the two directions
conf_matrix <- table(Switched = desc_switched, Original = desc_original)

# Add row and column totals to the matrix
conf_matrix_with_totals <- addmargins(conf_matrix, margin = c(1, 2), FUN = sum)
rownames(conf_matrix_with_totals)[length(relationship_levels) + 1] <- "Total (Switched)"
colnames(conf_matrix_with_totals)[length(relationship_levels) + 1] <- "Total (Original)"

# ========================================================
# Format Table: Bold Totals for LaTeX Output
# ========================================================
# Convert matrix entries to character to enable formatting
conf_matrix_bold <- apply(conf_matrix_with_totals, c(1, 2), as.character)

# Get dimensions of the matrix
n_rows <- nrow(conf_matrix_bold)
n_cols <- ncol(conf_matrix_bold)

# Bold last row (totals across rows) and last column (totals across columns)
conf_matrix_bold[n_rows, ] <- paste0("\\textbf{", conf_matrix_bold[n_rows, ], "}")
conf_matrix_bold[, n_cols] <- paste0("\\textbf{", conf_matrix_bold[, n_cols], "}")

# ========================================================
# Create and Export xtable for LaTeX
# ========================================================
# Convert formatted matrix to xtable object
latex_table <- xtable(
  conf_matrix_bold,
  caption = "Confusion Matrix of Relationship Descriptions (Columns: Original, Rows: Switched)",
  label = "tab:confusion"
)

# Define custom horizontal lines before and after totals row
addtorow <- list(
  pos = list(n_rows - 1, n_rows),
  command = c("\\hline\n", "\\hline\n")
)

# Print LaTeX-formatted table to console
print(
  latex_table,
  type = "latex",
  caption.placement = "top",
  include.rownames = TRUE,
  sanitize.text.function = identity,  # Allow raw LaTeX in cells (for \textbf)
  add.to.row = addtorow,
  hline.after = c(-1, 0, n_rows)  # Add lines above header, below header, and below table
)
