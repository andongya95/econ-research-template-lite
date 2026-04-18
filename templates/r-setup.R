# =============================================================
# r-setup.R — Standard R Project Setup
# Source at the top of every R script:
#   source(here::here("R", "r-setup.R"))
# =============================================================

# --- Reproducibility ---
set.seed(20240101)  # YYYYMMDD format — update per project

# --- Core packages ---
library(here)           # Relative paths via here::here()
library(tidyverse)      # Data wrangling + ggplot2
library(fixest)         # feols, fepois — fast FE estimation
library(modelsummary)   # Regression tables (LaTeX/HTML)
library(did)            # Callaway-Sant'Anna DiD estimator

# --- Output settings ---
options(scipen = 999)   # Suppress scientific notation in output
theme_set(theme_bw())   # Consistent ggplot2 theme

# --- Paths (all relative via here::here()) ---
RAW_DATA  <- here("data", "raw")
PROCESSED <- here("data", "processed")
RESULTS   <- here("results")
