# -------------------------------
# Setup: Working directory & packages
# -------------------------------
setwd("bipartite_representation_data")

# Define required packages
packages <- c("ggplot2", "mgcv", "scam", "CVXR", "patchwork", "data.table", "magrittr")

# Install 'infotheo' if not present
if (!requireNamespace("infotheo", quietly = TRUE)) install.packages("infotheo")
library(infotheo)
library(car)

# Install any other missing packages
new_pkgs <- packages[!(packages %in% installed.packages()[, "Package"])]
if(length(new_pkgs)) install.packages(new_pkgs)
lapply(packages, library, character.only = TRUE)

# Significance threshold
alfa = 10^(-5)

# -------------------------------
# Utility: Safe ANOVA p-value extractor
# -------------------------------
safe_anova_pval <- function(m1, m2) {
  a <- anova(m1, m2, test = "F")
  if ("Pr(>F)" %in% names(a) && !is.na(a$`Pr(>F)`[2]))
    return(a$`Pr(>F)`[2])
  else
    return(1)
}

# -------------------------------
# Main function: Analyze relationship between x and y
# -------------------------------
analyze_relationship <- function(x, y, direction_label, N = 10^4) {
  df <- data.frame(x = x, y = y)
  n <- nrow(df)
  
  # Subsample if data is too large
  if (n > N){
    set.seed(1)
    df <- df[sample(n, N), ]
  }
  
  # Fit models
  lm_model <- lm(y ~ x, data = df)  # Linear model
  lm_p <- summary(lm_model)$fstatistic
  p_lm <- pf(lm_p[1], lm_p[2], lm_p[3], lower.tail = FALSE)
  
  # Monotonic GAMs
  mono_inc <- scam(y ~ s(x, bs = "mpi"), data = df)
  mono_dec <- scam(y ~ s(x, bs = "mpd"), data = df)
  
  # Choose increasing or decreasing model
  mono_rss <- function(model) sum(resid(model)^2)
  increasing <- NA
  if (mono_rss(mono_inc) < mono_rss(mono_dec)) {
    monotonic_model <- mono_inc
    increasing <- TRUE
  } else {
    monotonic_model <- mono_dec
    increasing <- FALSE
  }
  
  # Unrestricted GAM
  gam_model <- gam(y ~ s(x, k = min(9, length(unique(x)))), data = df)
  
  # Compare models
  pval_mono_vs_lm <- safe_anova_pval(lm_model, monotonic_model)
  pval_gam_vs_mono <- safe_anova_pval(monotonic_model, gam_model)
  
  # Model predictions for plotting (commented out)
  # grid <- data.frame(x = seq(min(df$x), max(df$x), length.out = 200))
  # z <- qnorm(1-alfa/2)
  # add_preds <- function(model) {
  #   p <- predict(model, newdata = grid, se.fit = TRUE)
  #   fit <- p$fit
  #   data.frame(fit = fit, lower = fit - z * p$se.fit, upper = fit + z * p$se.fit)
  # }
  # preds <- cbind(
  #   grid,
  #   lm = add_preds(lm_model),
  #   mono = add_preds(monotonic_model),
  #   gam = add_preds(gam_model)
  # )
  
  # Classify relationship
  relationship <- NA
  relationship <- ifelse(
    pval_gam_vs_mono < alfa, "Non-monotonic",
    ifelse(pval_mono_vs_lm < alfa, "Monotonic",
           ifelse(p_lm < alfa, "Linear", "No relationship"))
  )
  
  # Correlation coefficients
  cor_pearson <- cor(df$x, df$y, method = "pearson", use = "complete.obs")
  cor_spearman <- cor(df$x, df$y, method = "spearman", use = "complete.obs")
  if (n > 10^5) {
    set.seed(1)
    df <- df[sample(n, 10^5), ]
  }
  cor_kendall <- cor(df$x, df$y, method = "kendall", use = "complete.obs")
  
  # Plotting code is present but commented out
  # (optional use for visual inspection or appendix generation)
  
  return(list(
    # plot = plot,
    summary = data.table(
      Direction = direction_label,
      `GAM vs Monotonic` = signif(pval_gam_vs_mono, 2),
      `Monotonic vs Linear` = signif(pval_mono_vs_lm, 2),
      `Linear F-test` = signif(p_lm, 2),
      N = n,
      Pearson = signif(cor_pearson, 2),
      Spearman = signif(cor_spearman, 2),
      Kendall = signif(cor_kendall, 2),
      Description = relationship,
      increasing = increasing
    )
  ))
}

# -------------------------------
# Batch processing of CSV files
# -------------------------------
csv_files <- list.files(pattern = "\\.csv$", full.names = TRUE)
csv_files  # List files to verify

dir.create("plots_appendix", showWarnings = FALSE)

rm(summary_table)  # clear any existing object
counter <- 1  # progress counter

# Loop over all files and run the analysis
summary_table <- rbindlist(lapply(csv_files, function(file) {
  df <- fread(file)
  print(paste(counter, file))
  counter <<- counter + 1
  
  if (!all(c("degrees", "he_sizes") %in% names(df))) return(NULL)
  
  # Optional: degrees → he_sizes direction
  # a1 <- analyze_relationship(df$degrees, df$he_sizes, "degrees → he_sizes", N=2*10^6)
  
  # Main analysis: he_sizes → degrees direction
  a2 <- analyze_relationship(df$he_sizes, df$degrees, "he_sizes → degrees", N=2*10^6)
  
  # Optional plotting and saving (commented out)
  # combined_plot <- a2$plot + plot_annotation(title = sub("^assortativity_(.*)\\.csv$", "\\1", basename(file)))
  # ggsave(filename = file.path("plots3", paste0(tools::file_path_sans_ext(basename(file)), ".png")),
  #        plot = combined_plot, width = 7, height = 7)
  
  rbind(
    # Optionally include a1$summary here
    cbind(Hypergraph = basename(file), a2$summary)
  )
}))

# Save summary results
fwrite(summary_table, "data/relationship_summary3_direction.csv")

# -------------------------------
# Model validation and residuals
# -------------------------------
# Compute absolute and directional difference between Pearson and Spearman
merged_df$spearson_absdiff <- abs(merged_df$Pearson - merged_df$Spearman)
merged_df$spearson_diff <- merged_df$Spearman - merged_df$Pearson

# Sort by absolute difference
merged_df[order(merged_df$spearson_absdiff),]

# Linear model: Spearman as function of Pearson
model <- lm(Spearman ~ Pearson, data = merged_df)
summary(model)

# Hypothesis test: is intercept = 0 and slope = 1?
linearHypothesis(model, c("(Intercept) = 0", "Pearson = 1"))
