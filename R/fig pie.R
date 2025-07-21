# ========================================================
# Load Required Package
# ========================================================
library(ggplot2)  # For data visualization

# ========================================================
# Prepare Relationship Category Data
# ========================================================
# Define relationship categories and their counts (reverse order for plotting)
categories <- c("No relationship", "Linear", "Monotonic", "Non-monotonic")[4:1]
counts <- c(3, 6, 12, 15)[4:1]

# Compute total and percentages
total <- sum(counts)
percentages <- round(100 * counts / total, 0)

# Create a data frame with counts and percentages
bar_data <- data.frame(
  Category = factor(categories, levels = categories),  # Factor for correct ordering
  Count = counts,
  Percentage = percentages
)

# ========================================================
# Bar Chart: Counts and Percentages
# ========================================================
ggplot(bar_data, aes(x = Category, y = Count, fill = Category)) +
  geom_bar(stat = "identity") +  # Use actual counts
  geom_text(
    aes(label = paste0(Count, " (", Percentage, "%)")),  # Add count + percentage labels
    vjust = -0.5,
    size = 4
  ) +
  theme_minimal() +
  labs(
    title = "Distribution of Relationship Categories",
    x = "",
    y = "Count"
  ) +
  theme(legend.position = "none")  # Remove redundant legend

# ========================================================
# Pie Chart: Visualizing Proportions
# ========================================================
# Create labels combining category, count, and percentage
pie_data <- bar_data
pie_data$Label <- paste0(pie_data$Category, "\n", pie_data$Count, " (", pie_data$Percentage, "%)")

# Create pie chart using polar coordinates
pie <- ggplot(pie_data, aes(x = "", y = Count, fill = Category)) +
  geom_bar(stat = "identity", width = 1) +        # Bar heights = counts
  coord_polar(theta = "y") +                      # Convert bar chart to pie chart
  labs(title = "Only 3 of 36 Empirical Hypergraphs (8%) Show\nNo Relationship Between Hyperedge Size and Degree") +
  theme_void() +                                  # Remove axes/grid
  geom_text(
    aes(label = Label),
    position = position_stack(vjust = 0.5),       # Center labels in each slice
    size = 4
  ) +
  theme(legend.position = "none")  # Remove legend (info is on slices)

# ========================================================
# Save the Pie Chart
# ========================================================
ggsave(
  filename = file.path("plots", "pie.png"),
  plot = pie,
  width = 7,
  height = 7
)
