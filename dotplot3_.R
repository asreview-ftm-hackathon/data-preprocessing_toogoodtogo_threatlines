# using rbokeh for interaction and tooltips

# install.packages("readr")
# install.packages("lubridate")
# install.packages("rbokeh")
library("readr")
library("dplyr")
library("stringr")
library("lubridate")
library("rbokeh")

fn <- file.path("data", "split_emails.csv")
data <- read_delim(fn, delim = "|")

mail <- data %>% filter(doc_type == "Mail") %>%
  filter(betterDate >= ymd(20160101) & betterDate < ymd(20200101)) %>%
  group_by(doc_id) %>%
  mutate(thread_length = n(),
         thread_start = min(betterDate)) %>%
  ungroup() %>%
  filter(thread_length > 1) %>%
  arrange(thread_start, doc_id) %>%
  group_by(thread_start) %>%
  mutate(thread_seq = cur_group_id(),
         thread_gp = 1 + trunc(thread_seq / 16)) %>%
  ungroup() %>%
  mutate(id = as.factor(doc_id),
         year = year(betterDate),
         quarter = trunc(1 + month(betterDate) / 4),
         month = month(betterDate))

ylim <- levels(with(mail, reorder(id, betterDate)))
p <- figure(ylim = ylim, data = mail, width = 800, height = 800) %>%
  ly_points(x = "betterDate", y = "id",
            hover = c("title", "betterDate"), size = 4)
p

