library(dplyr)
library(lubridate)
library(stringr)
setwd('/home/jmontero/Documents/auto_search/')

df <- read.csv('dataframes/all_cars.csv', colClasses = c(NA, "Date", rep(NA, 9)))
df <- df[df$year >= 2013 & df$spot_price <=50000, ]
# cvs <- str_match(tolower(df$title), '(\\d+)cv')
# df$cv <-cvs[1:nrow(cvs), 2]
# df$cv <- type.convert(df$cv, 'numeric')
df$date_yday <- yday(df$date) - 1  # only valid if same year!
df$year_old <- 2021 - df$year
df$year_old_sq <- df$year_old^2
df$auto <- grepl('AUTO', df$title, ignore.case = T)
df$VX <- grepl('VX[^L]', df$title, ignore.case = T, perl=T)
df$VXL <- grepl('VXL', df$title, ignore.case = T, perl=T)
df$GX <- grepl('GX', df$title, ignore.case = T, perl=T)
df$land_cruiser_5p <- grepl('land_cruiser_5p', df$page, perl=T)
df$rr <- grepl('land_rover_rr', df$page)
df$range_rover_sport <- grepl('land_rover_range_rover_sport', df$page)
df$tdv6 <- grepl('TDV6', df$title, ignore.case = T, perl=T) & df$range_rover_sport
df$grand_cherokee <- grepl('grand_cherokee', df$page)
df$overland <- grepl('overland', df$title, ignore.case = T)
df$kilometrage_sq <- df$kilometrage^2
df$kilometrage_year <- df$kilometrage / df$year_old
df$kilometrage_year_sq <- df$kilometrage_year ^ 2
# df <- df[df$VX | df$VXL | df$GX | df$range_rover_sport | df$rr | df$land_cruiser_5p, ]

# drop outlier in overland
df <- df[!(df$overland & df$spot_price == 25499), ]
df <- df[!(df$overland & df$spot_price == 26599), ]

# with all variables
write.csv(df, "dataframes/cars_with_indicators.csv")


model_df <- df %>% 
              select(-c('financed_price', 'date', 'location', 'page'))
# model_df <- df[, c('spot_price', 'kilometrage', 'kilometrage_sq', 'kilometrage_year', 'year',
#                    'year_old', 'VXL', 'VX', 'auto', 'office','warranty', 'type_petrol', 'rr', 'land_cruiser_5p',
#                    'range_rover_sport', 'tdv6', 'grand_cherokee', 'overland')]
model_df <- na.omit(model_df)
# df$LIMITED <- grepl('LIMITED', df$title, ignore.case = T, perl=T)
# currently, date is excluded
model <- lm(spot_price ~ kilometrage + kilometrage_sq
            + kilometrage_year + kilometrage_year_sq + year_old + year_old_sq + VXL + VX + auto 
            + warranty + type_petrol + office + range_rover_sport + tdv6 + rr + land_cruiser_5p
            + grand_cherokee + overland, model_df)
model_df$residuals <- model$residuals

selected_df <- model_df %>%
                filter(kilometrage <= 125000 & year >=2015 &spot_price <=35000) %>% 
                arrange(residuals)

selected_df <- selected_df %>% 
  left_join(df) %>% 
  distinct(title, location, spot_price, kilometrage, residuals) %>% 
  head(20)

selected_df

selected_df_complete <- model_df %>%
  filter(kilometrage <= 125000 & year >=2015 &spot_price <=35000 & date_yday >= 238) %>% 
  arrange(residuals) %>% 
  head(50)

selected_df_complete <- selected_df %>% 
  left_join(df) %>% 
  head(20)

# selected_df_complete