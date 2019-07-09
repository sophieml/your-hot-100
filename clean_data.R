library(tidyverse)
library(ISOweek)
library(lubridate)
setwd("~/your-hot-100")
data <- read_csv("data.csv")

data$date_uts <- as.integer(data$date_uts)

data <- data %>% 
  mutate(week = strftime(as.POSIXct(as.numeric(data$date_uts), origin="1970-01-01")
                         , "%V"))

missing_obs <- data.frame(artist = rep(unique(data$artist), max(data$week)),
                          week = rep(as.character(1:max(data$week)), each = length(unique(data$artist))),
                          n = 0)

by_week <- data %>% 
  group_by(artist, week) %>% 
  summarize(n = n()) %>% 
  ungroup()

by_week <- complete(by_week, artist, nesting(week), fill = list(n = 0))

by_week <- by_week %>% 
  group_by(artist) %>% 
  mutate(total_n = cumsum(n)) %>% 
  arrange(week, desc(total_n)) %>% 
  mutate(week_start = ISOweek2date(paste0("2019-W", week, "-1")) - 1,
         week_end = ISOweek2date(paste0("2019-W", week, "-7")) - 1) %>% 
  mutate(week_str = paste0(strftime(week_start, "%b %d"), "-", strftime(week_end, "%b %d"))) %>% 
  select(-week_start, -week_end)

top10_by_week <- by_week %>% 
  group_by(week) %>% 
  arrange(week, desc(total_n)) %>% 
  slice(c(1:10))

write_csv(by_week, "data_by_week.csv")
write_csv(top10_by_week, "top10_by_week.csv")

for_d3 <- by_week %>% 
  mutate(week = as.integer(week)) %>% 
  filter(artist %in% unique(top10_by_week$artist)) %>% 
  select(artist, week, total_n) %>% 
  reshape2::dcast(artist ~ week)

write_csv(for_d3, "for_d3.csv")


