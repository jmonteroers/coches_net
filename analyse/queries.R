setwd('/home/jmontero/Documents/auto_search/')
df <- read.csv('dataframes/cars_with_indicators.csv')

# resultados 2/9/20, toyota y rr_sport
# Toyota azul feo
query_df_1 <- df %>% 
  filter(spot_price == 40500, kilometrage == 3000, VX == T)
query_df_1

# Range Rover Sport, se ve bien
query_df_2 <- df %>% 
  filter(spot_price == 44900, kilometrage == 45726, range_rover_sport == T)
query_df_2

# el de Asturias, antiguo
query_df_3 <- df %>% 
  filter(spot_price == 36900, kilometrage == 14000, VX == T)
query_df_3

# automobiles Martin
query_df_4 <- df %>% 
  filter(spot_price == 30000, kilometrage == 39000, VX == T)
query_df_4

# el de Madrid
query_df_5 <- df %>% 
  filter(spot_price == 34000, kilometrage == 66000, VX == T)
query_df_5



# resultados 2/9, con toyotas 5 plazas
# onubense, maletero no se ve bien
query_df_3 <- df %>% 
  filter(spot_price == 28000, kilometrage == 56000, land_cruiser_5p == T)
query_df_3

query_df_4 <- df %>% 
  filter(spot_price == 33000, kilometrage == 35000, land_cruiser_5p == T)
query_df_4

query_df_9 <- df %>% 
  filter(spot_price == 31900, kilometrage == 52507, land_cruiser_5p == T)
query_df_9


# resultados 3/9, con grand cherokees
# el de Sevilla con autoHero
query_df_1 <- df %>% 
  filter(spot_price == 26599, kilometrage == 44828, grand_cherokee == T)
query_df_1
# el Toyota azul feo
query_df_2 <- df %>% 
  filter(spot_price == 40500, kilometrage == 3000, VX == T)
query_df_2
# Grand Cherokee en Tarragona
query_df_3 <- df %>% 
  filter(spot_price == 28900, kilometrage == 83149, grand_cherokee == T)
query_df_3


# 3/9: mas antiguos, recientes
query_df_2 <- df %>% 
  filter(spot_price==24500, kilometrage == 69650, grand_cherokee == T)
query_df_2
