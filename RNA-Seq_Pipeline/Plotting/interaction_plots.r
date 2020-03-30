library("DESeq2")
library("ggplot2")

npg <- 20
mu <- 2^c(8,10,9,11,10,12)
condition <- rep(rep(c("A","B"),each=npg),3)
genotype <- rep(c("I","II","III"),each=2*npg)
countData <- data.frame()
N_G1 = 10
for(i in 1:N_G1){
  counts <- rnbinom(6*npg, mu=rep(mu,each=npg), size=1/.01)
  countData <- rbind(countData, as.integer(counts))
}
colnames(countData) <- paste0("S",seq(1,dim(countData)[2]))

mu[4] <- 2^12
mu[6] <- 2^8
N_G2 = 10
for(i in 1:N_G2){
  counts <- rnbinom(6*npg, mu=rep(mu,each=npg), size=1/.01)
  countData <- rbind(countData, as.integer(counts))
}

mu <- 2^c(8,8,9,9,10,10)
N_G3 = 100
for(i in 1:N_G3){
  counts <- rnbinom(6*npg, mu=rep(mu,each=npg), size=1/.01)
  countData <- rbind(countData, as.integer(counts))
}

Names_G1 <- paste0(rep("G1.", N_G1), seq(1,N_G1))
Names_G2 <- paste0(rep("G2.", N_G2), seq(1,N_G2))
Names_G3 <- paste0(rep("G3.", N_G3), seq(1,N_G3))

rownames(countData) <- c(Names_G1, Names_G2, Names_G3)
colData <- as.data.frame(cbind(condition, genotype))
rownames(colData) <- colnames(countData)

dds <- DESeqDataSetFromMatrix(countData = countData,
                              colData   = colData,
                              design    = ~ genotype + condition + genotype:condition)

dds <- DESeq(dds, fitType='local')


# Plots of one sample for each simulated gene set
plot_log2fc <- function(d, title) {
  ggplot(d, aes(x=cond1, y=log2c, group=cond2)) +
    geom_jitter(size=1.5, position = position_jitter(width=.15)) +
    facet_wrap(~ cond2) +
    stat_summary(fun.y=mean, geom="line", colour="red", size=0.8) +
    xlab("cond1") + ylab("log2(counts+1)") + ggtitle(title)
}

log2c_all <- t(log2(counts(dds) + 1))
g_names = c('G1.1','G2.1','G3.1')
all_plots <- list()
pdf("Simulated_Data_With_Null_Genes.pdf")
for(g_name in g_names){
  log2c = log2c_all[,g_name]
  d <- data.frame(log2c = log2c, cond1 = colData(dds)$cond1, cond2 = colData(dds)$cond2)
  all_plots[[g_name]] <- plot_log2fc(d, g_name)
  print(all_plots[[g_name]])
}
graphics.off()

pdf("Simulated_Data_With_Null_Genes1.pdf")
for(g_name in g_names1){
  log2c = log2c_all[,g_name]
  d <- data.frame(log2c = log2c, cond1 = colData(dds)$cond1, cond2 = colData(dds)$cond2)
  all_plots[[g_name]] <- plot_log2fc(d, g_name)
  print(all_plots[[g_name]])
}
graphics.off()

resultsNames(dds)

# the interaction term for condition effect in genotype II vs genotype I.
# this tests if the condition effect is different in II compared to I
res21 <- results(dds, name="genotypeII.conditionB")
res21[grepl('G1.', rownames(res21)),]
res21[grepl('G2.', rownames(res21)),]

# the interaction term for condition effect in genotype III vs genotype I.
# this tests if the condition effect is different in III compared to I
res31 <- results(dds, name="genotypeIII.conditionB")
res31[grepl('G1.', rownames(res31)),]
res31[grepl('G2.', rownames(res31)),]

# the interaction term for condition effect in genotype III vs genotype II.
# this tests if the condition effect is different in III compared to II
res32 <- results(dds, contrast=list("genotypeIII.conditionB", "genotypeII.conditionB"))
res32[grepl('G1.', rownames(res32)),]
res32[grepl('G2.', rownames(res32)),]