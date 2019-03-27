library(readr)
library(rvest)

urls <- c('https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_artificialintelligence',
          'https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_bioinformatics',
          'https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_computationallinguistics',
          'https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_computergraphics',
          'https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_computernetworkswirelesscommunication',
          'https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_computersecuritycryptography',
          'https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_computervisionpatternrecognition',
          'https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_computingsystems',
          'https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_datamininganalysis',
          'https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_databasesinformationsystems',
          'https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_humancomputerinteraction',
          'https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_informationtheory',
          'https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_medicalinformatics',
          'https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_multimedia',
          'https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_robotics',
          'https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_signalprocessing',
          'https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_softwaresystems',
          'https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_theoreticalcomputerscience')

communities <- c('ai', 
                 'bioinformatics', 
                 'computational linguistics', 
                 'graphics', 
                 'networks', 
                 'security', 
                 'vision',
                 'systems', 
                 'data mining', 
                 'databases',
                 'hci',
                 'information theory',
                 'medical informatics',
                 'multimedia',
                 'robotics',
                 'signal processing',
                 'software systems',
                 'theory')

df <- data.frame()

for (i in 1:length(urls)) {
    url <- urls[i]
    community <- communities[i]
    table_page <- url %>% read_html() %>% html_table()
    table_page <- table_page[[1]]
    df <- rbind(df,as.data.frame(cbind(table_page$Publication, rep(community, length(table_page$Publication)))))
}

names(df) <- c("venue", "community")
df$venue <- tolower(df$venue)
write_csv(df, "scraped_communities.csv")