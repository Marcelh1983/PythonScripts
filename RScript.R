args <- commandArgs(trailingOnly = TRUE)
csvData <- read.csv(file=file.path(getwd(), args[1]), header=TRUE, sep=";")
result <- paste("read ", nrow(csvData), ' items')
cat(result)