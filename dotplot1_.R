# script to read data

# install.packages("readr")
# install.packages("lubridate")
library("readr")
library("dplyr")
library("stringr")
library("ggplot2")

fn <- file.path("data", "split_emails.csv")
data <- read_delim(fn, delim = "|")

mail <- data %>% filter(doc_type == "Mail") %>%
  filter(betterDate >= ymd(20140101) & betterDate < ymd(20200101)) %>%
  group_by(doc_id) %>%
  mutate(thread_length = n()) %>%
  filter(thread_length > 1)

g <- ggplot(mail, aes(x = betterDate, y = reorder(doc_id, betterDate))) +
  geom_point(size = 0.7) +
  theme_classic()
g
