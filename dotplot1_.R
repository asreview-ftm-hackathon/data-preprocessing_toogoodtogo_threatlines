# script to read data

install.packages("readr")
library("readr")
library("dplyr")
library("ggplot2")

fn <- file.path("data", "split_emails.csv")
data <- read_delim(fn, delim = "|")

mails <- data %>% filter(type == "Mail")

g <- ggplot(mails, aes(x = betterDate, y = reorder(title, betterDate))) +
  geom_point(size = 2) +
  theme_light() +
  theme(axis.text.x = element_text(angle = 60, hjust = 1))

