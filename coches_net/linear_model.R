library(dplyr)
library(lubridate)
library(stringr)

#' Prepare Ads for Analysis
#'
#' Reads dataframe from \code{filename}, and prepares it for statistical analysis. 
#' In particular, it creates the variables:
#' \itemize{
#'   \item{hp}{horsepower. Extracted from title, therefore, unreliable}
#'   \item{date_yday}{day of the year when ad was published}
#'   \item{year_old}{how old the car is}
#'   \item{year_old_sq}{the square of \code{year_old}}
#'   \item{auto}{whether the car has automatic transmission. Extracted from title, therefore, unreliable}
#'   \item{kilometrage_sq}{the square of kilometrage}
#'   \item{kilometrage_per_year}{kilometrage divided by year_old + 1 (to avoid division by zero)}
#'   \item{kilometrage_per_year_sq}{kilometrage_per_year squared}
#' }
#'
#' Note that it also omits rows with NAs.
#' 
#' @param filename name of the csv file where the dataframe is stored
#' @param min_year minimum year to restrict car ads sample to
#' @param max_spot_price maximum spot price to restrict sample to
#'
#' @return dataframe prepared for statistical analysis
#' 
#' @notes for large dataframes, could add an optional month effect
prepare_ads_for_analysis <- function(filename, min_year = 2013, max_spot_price = 50000) 
{
  # assume that second column is date
  df <- read.csv(filename, colClasses = c(NA, "Date", rep(NA, 9)))
  # restrict sample
  df <- df[df$year >= min_year & df$spot_price <=max_spot_price, ]
  # add hp to dataframe (cv in Spanish)
  hps <- str_match(tolower(df$title), '(\\d+)cv')
  df$hp <-hps[, 2]
  df$hp <- type.convert(df$hp, 'numeric')
  # add more variables
  df$date_yday <- yday(df$date) - 1  # only valid if same year!
  df$year_old <- 2020 - df$year
  df$year_old_sq <- df$year_old^2
  df$auto <- grepl('AUTO', df$title, ignore.case = T)
  df$kilometrage_sq <- df$kilometrage^2
  df$kilometrage_per_year <- df$kilometrage / (df$year_old + 1)
  df$kilometrage_per_year_sq <- df$kilometrage_per_year ^ 2
  # omit NAs
  df <- na.omit(df)
  return(df)
}

#' Convert characters to formula for lm
#' 
#' Trick extracted from https://stackoverflow.com/questions/4951442/formula-with-dynamic-number-of-variables
#' 
#' @param dep_var character, name of dependent variable
#' @param char_vec character vector with regressors
#' 
#' @return character vector transformed to formula
from_vec_to_formula_lm <- function(dep_var, regressors) {
  as.formula(paste(dep_var, "~", paste(regressors, collapse = "+")))
}


#' Fit linear model, return ads with lowest residuals
#' 
#' Allows user to determine the variables of the linear model. After running the regression,
#' selects the columns in \code{columns_to_select} and outputs the \code{show_first_n} distinct
#' observations.
#' 
#' @param df dataframe with variables prepared to run a linear regression
#' @param dep_var character, name of dependent variable in linear regression
#' @param regressors character vector with name of regressors
#' @param columns_to_select character vector with name of columns to preserve in output dataframe
#' @param show_first_n number of distinct ads to keep in output dataframe. Default is 20
#' 
#' @return dataframe with \code{show_first_n} ads ordered from lowest to largest residual. In other words,
#' from the most to the least undervalued ad.
run_residual_analysis <- function(df, dep_var = "spot_price",
                                  regressors = c("kilometrage", "kilometrage_sq",
                                                 "kilometrage_year", "kilometrage_per_year_sq", 
                                                  "year_old", "year_old_sq", "auto", 
                                                 "warranty", "type_petrol", "office"),
                                  columns_to_select = c("title", "location", "spot_price", 
                                                        "kilometrage", "residuals"),
                                  show_first_n=20)
{
  formula_lm <- from_vec_to_formula_lm(dep_var = dep_var,
                                       regressor = regressors)
  model <- lm(formula_lm, df)
  df$residuals <- model$residuals
  df %>%
    arrange(residuals) %>% 
    select(columns_to_select) %>% 
    distinct() %>% 
    head(show_first_n)
}