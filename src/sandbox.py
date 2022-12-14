import rpy2
from rpy2.robjects.packages import importr

commands_to_run = """
#adjust working directory
getwd()
setwd("C:/Users/lukac/PycharmProjects/SD_scenario_analysis_anti_bug/BBSD-Public-master/Budworms")
wd <- getwd()

#load functions
source("../20180819_BBSD_R_Functions_original.R")

#load libraries
library("arrow")
require("ggplot2")

#load data
data_date <- "2022-08-02"
outcome <- "x"
experiments <- "Experiments"

path_outcomes <- paste(wd,"/Data/", data_date,outcome,".feather", sep="")
path_experiments <- paste(wd,"/Data/", data_date,experiments,".feather", sep="")

df_expts <- read_feather(path_experiments)
df_outcomes <- read_feather(path_outcomes)

#get clustering solutions for a given k value 
cl_methods <- c("CID")

df_cl3 <- get.clusters.df(df_outcomes,cl_methods,3)

colnames(df_expts)

#copy subspace limits from EMA Workbench in Python for boxes of choice
#difficult to generalize this plot creation, therefore best to build manually
SubspacesCID_PRIM <- ggplot(df_expts, aes(r0,rstep))+geom_point(aes(color=as.factor(df_cl3$CID))) + 
  labs(color="Cluster",x="r",y="rstep") +
  geom_rect(aes(xmin = 0.503822, xmax = 0.686619, ymin = 0.261795, ymax = 0.399527 ),color = 'darkred', alpha=0) +
  geom_rect(aes(xmin = 0.450066, xmax = 0.532534, ymin = -Inf, ymax = Inf),color = 'darkgreen', alpha=0) +
  geom_rect(aes(xmin = 0.563886, xmax = 0.699330, ymin = 0.101276, ymax = 0.268418),color = 'darkblue', alpha=0)

plot(SubspacesCID_PRIM)

#save plot
saveloc <- paste(wd,"/Figures/",Sys.Date(),"-Budworms-CID-Subspaces.png",sep="")
ggsave(plot = SubspacesCID_PRIM, saveloc, h = 5, w = 6, type = "cairo-png")

"""
rpy2.robjects.r(commands_to_run)
deb=0