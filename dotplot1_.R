# script to read data

install.packages("readr")
library("readr")
library("dplyr")
library("stringr")
library("ggplot2")

fn <- file.path("data", "split_emails.csv")
data <- read_delim(fn, delim = "|")

mail <- data %>% filter(type == "Mail") %>%
  filter(betterDate >= ymd(20140101) & betterDate < ymd(20200101)) %>%
  group_by(id) %>%
  mutate(thread_length = n()) %>%
  filter(thread_length > 1)

g <- ggplot(mail, aes(x = betterDate, y = reorder(id, betterDate))) +
  geom_point(size = 1) +
  theme_linedraw() +

  theme(axis.text.x = element_text(angle = 0, hjust = 1))

