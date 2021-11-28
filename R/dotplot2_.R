# using trelliscope for interaction

# install.packages("readr")
# install.packages("lubridate")
# install.packages("trelliscopejs")
# install.packages("plotly")
library("readr")
library("dplyr")
library("stringr")
library("lubridate")
library("trelliscopejs")
library("plotly")
library("ggplot2")


fn <- file.path("data", "split_emails.csv")
data <- read_delim(fn, delim = "|")

mail <- data %>% filter(doc_type == "Mail") %>%
  filter(betterDate >= ymd(20140101) & betterDate < ymd(20200101)) %>%
  group_by(doc_id) %>%
  mutate(thread_length = n()) %>%
  filter(thread_length > 1)

theme_set(theme_classic())
theme_update(panel.background = element_rect(fill = "transparent", colour = NA),
             plot.background = element_rect(fill = "transparent", colour = NA),
             legend.key = element_blank(),
             rect = element_rect(fill = "transparent") # all rectangles
)

mail <- data %>% filter(doc_type == "Mail") %>%
  filter(betterDate >= ymd(20160101) & betterDate < ymd(20200101)) %>%
  group_by(doc_id) %>%
  mutate(id = as.factor(doc_id),
         thread_length = n(),
         thread_start = min(betterDate)) %>%
  ungroup() %>%
  filter(thread_length > 1) %>%
  arrange(thread_start, doc_id) %>%
  group_by(thread_start) %>%
  mutate(thread_seq = cur_group_id(),
         thread_gp = 1 + trunc(thread_seq / 16)) %>%
  ungroup() %>%
  mutate(year = year(betterDate),
         quarter = trunc(1 + month(betterDate) / 4),
         month = month(betterDate))

g <- ggplot(mail, aes(x = betterDate, y = reorder(id, thread_seq)), name = ) +
  geom_point(size = 0.7) +
  scale_y_discrete("Thread number") +
  geom_point(
    size = 0.7,
    shape = 1,
    aes(text = title, text2 = abstract)) +
  facet_trelliscope(
    vars(thread_gp),
    name = "Thread by Date",
    ncol = 1,
    nrow = 1,
    data = mail,
    scales = "free",
    path = "dotplot2",
    as_plotly = TRUE) +
  theme(legend.position = "none")

g

