# plots the differences in fold changes or counts for a treatment effect over two conditions 
# there are two options to do this, either using a DESeq2 dds object or by providing data manually
# updated 180518 by Ronald Cutler

require("ggplot2")

# set the directory to write a pdf out to CHANGE THIS
dir = "/Users/margaretsaha/Desktop/temp"

# this function plots the counts which are then grouped by subgenome
plot_log2fc_subgenome <- function(d, title) 
{
  ggplot(d, aes(x=condition, y=log2c, group=subgenome)) +
    geom_jitter(size=3, position = position_jitter(width=.2)) +
    facet_wrap(~ subgenome) +
    stat_summary(fun.y=mean, geom="line", colour="red", size=0.8) +
    xlab("Condition") + ylab("Normalized log2(counts+1)") + 
    ggtitle(title) +
    theme(axis.text = element_text(size = 12),
          axis.title.x = element_text(size = 14, face = "bold"),
          axis.title.y = element_text(size = 14, face = "bold"),
          strip.text.x = element_text(size = 14),
          title = element_text(size = 16, face = "bold"),
          strip.background = element_blank())
}

# this function plots the counts which are then grouped by condition
plot_log2fc_condition <- function(d, title) 
{
  ggplot(d, aes(x=subgenome, y=log2c, group=condition)) +
    geom_jitter(size=3, position = position_jitter(width=.2)) +
    facet_wrap(~ condition) +
    stat_summary(fun.y=mean, geom="line", colour="red", size=0.8) +
    xlab("Subgenome") + ylab("Normalized log2(counts+1)") + 
    ggtitle(title) +
    theme(axis.text = element_text(size = 12),
          axis.title.x = element_text(size = 14, face = "bold"),
          axis.title.y = element_text(size = 14, face = "bold"),
          strip.text.x = element_text(size = 14),
          title = element_text(size = 16, face = "bold"),
          strip.background = element_blank()) 
    
}

#####if using DESeq2 output object use this####

g_names = c() # gene names of interest go here
log2c_all <- t(log2(counts(dds) + 1, normalized = TRUE)) # dds object goes here
all_plots <- list() # list to hold plots

# plotting and writing out. this uses the subgenome type plot function
pdf(dir)
for(g_name in g_names)
{
  log2c = log2c_all[,g_name]
  d <- data.frame(log2c = log2c, condition = colData(dds18)$condition, stage = colData(dds18)$subgenome)
  all_plots[[g_name]] <- plot_log2fc_subgenome(d, g_name)
  print(all_plots[[g_name]])
}
graphics.off()


####if using counts provide the data manually####

# in the first column named 'log2c, the condition in the second column named 'condition' and the subgenome in the last column named 'subgenome'
# below is an example where we compare L and S homeologs across 3 different conditions

g_name <- "test" # set this to the gene name
log2c <- c(20.68455756,	23.54896941,	26.68902313,	6.135332629,	13.73194256,	10.65489387,	36.64455361,	35.24600758,	26.557262,	6.447694126,	12.67701011,	17.21169947,	26.7894932,	154.4379189,	70.50652381,	49.15218058,	52.07953405,	61.42026705) # counts go here
condition <- rep(c("DBM", "GFP", "ICD"), each = 6) # condition goes here - we are repeating "DBM", "GFP", "ICD" each 6 times
subgenome <- rep(rep(c("L", "S"), each = 3), times = 3) # subgenome goes here - we are repeating "L", "S" each 3 times and then repeating that sequence 3 times

# plotting and writing out
d <- data.frame(log2c = log2c, condition = condition, subgenome = subgenome)

# here we use both plotting functions and pick whichever one we like
plot_log2fc_subgenome(d, g_name)
plot_log2fc_condition(d, g_name)
