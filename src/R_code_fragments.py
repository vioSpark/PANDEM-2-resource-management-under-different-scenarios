import warnings

import os

os.environ["R_HOME"] = r"C:\Program Files\R\R-4.2.1"
import rpy2
from rpy2.robjects.packages import importr
import datetime


class RInterface:
    possible_clustering_methods = ["ACF", "CID", "CORT", "DWT", "LLR", "LPC", "PDC", "PER", "PIC", "DTW", "SBD", "GAK",
                                   "TAD", "LCM"]
    # Willem knows no difference in these
    unsupported_clustering_methods = ["DWT", "LCM"]

    def __init__(self, outcomes_folder_path: str, experiments_file_path: str, clustering_methods_to_perform):
        """
        :param: clustering_methods_to_perform: The type of clustering methods we are interested in for analysis
        (used both in the clustering and the plot_silhouettes steps)
        """
        # TODO: fix up silhouette plotting
        if not all(item in self.possible_clustering_methods for item in clustering_methods_to_perform):
            # choose from ["ACF","CID","CORT","DWT","LLR","LPC","PDC","PER","PIC","DTW","SBD","GAK","TAD","LCM"]
            raise ValueError("unsupported clustering method")

        if any(item in clustering_methods_to_perform for item in self.unsupported_clustering_methods):
            # DWT distance calculation is unsupported temporarily,
            # author doesn't recommend LCM (latent class Markov model clustering)
            warnings.warn("unrecommended clustering method, consider using an alternate one")

        self.outcomes_file_path = outcomes_folder_path.replace('\\', '/')
        self.experiments_file_path = experiments_file_path.replace('\\', '/')

        if clustering_methods_to_perform is not None:
            tmp = ''
            for method in clustering_methods_to_perform:
                tmp += '"' + method + '", '
            self.clustering_methods_to_perform = '(' + tmp[0:-2] + ')'
        else:
            self.clustering_methods_to_perform = "()"

        self.commands_to_run = ""
        self.initialize_r_environment()
        self.run()
        # make this a logging
        print('R started, cwd is at:', rpy2.robjects.r("getwd()"))

    def initialize_r_environment(self):
        self.commands_to_run += '''
        #load functions R file
        source("./20180819_BBSD_R_Functions.R")

        #load libraries
        library("arrow")
        require("reshape2")
        require("ggplot2")

        #load data
        data_date <- "''' + (str(datetime.date.today())) + '''"
        outcome <- "I[g1, Isolated]"
        experiments <- "experiments"
        wd <- getwd()

        path_outcomes_folder <- "''' + self.outcomes_file_path + '''"
        path_experiments <- "''' + self.experiments_file_path + '''"
        
        df_expts <- read_feather(path_experiments)
        cl_methods <- c''' + self.clustering_methods_to_perform + "\n"

    def run(self):
        result = rpy2.robjects.r(self.commands_to_run)
        self.commands_to_run = ""
        return result

    def plot_all_scenarios(self, save_file_path):
        self.commands_to_run += """
        #plot time series
        ts_plot <- plot.timeseries(df_outcomes)
        plot(ts_plot)
        
        #export plot
        loc <- paste(wd,"/Figures/",Sys.Date(),"-Budworms","Exploration.png",sep="")
        ggsave(plot = ts_plot, """ + save_file_path + """, h = 6, w = 8, type = "cairo-png")
        """

    def calculate_and_plot_silhouettes(self, outcome: str,
                                       maximum_cluster_count: int,
                                       plot_save_path: str,
                                       data_save_path: str):
        plot_save_path = plot_save_path.replace('\\', '/')
        data_save_path = data_save_path.replace('\\', '/')
        # calculate and save data
        self.commands_to_run += '''
        # load experiments
        path_outcomes <- paste(path_outcomes_folder, "/", "''' + outcome + '''",sep="")
        df_outcomes <- arrow::read_feather(path_outcomes)
        
        df_sils <- compare.silhouettes(df_outcomes,cl_methods,2,''' + str(maximum_cluster_count) + ''',logging=TRUE)
        write_feather(df_sils, "''' + data_save_path + '''")
        '''

        # plot and save plot
        self.commands_to_run += '''
        # save silhouette trajectories to the disk
        png(file="''' + plot_save_path + '''", width=600, height=350)
        df_sils_long <- melt(df_sils, id.vars = c("k"), variable.name = "method")
        sils_plot <- ggplot(df_sils_long, aes(x=k, y=value, color=method, group=method)) + geom_point() +
        geom_line() + xlab("k") + ylab("silhouette width")

        plot(sils_plot)
        dev.off()
        '''

    def make_clusters(self, outcome: str, number_of_clusters: int):
        self.commands_to_run += '''
        path_outcomes <- paste(path_outcomes_folder, "/", "''' + outcome + '''",sep="")
        df_outcomes <- arrow::read_feather(path_outcomes)
        
        df_cl3 <- get.clusters.df(df_outcomes, cl_methods,''' + str(number_of_clusters) + ")\n"

    def plot_clusters(self, outcome: str, path_to_clusters_file: str, folder_to_save: str, clustering_method: str,
                      amount_of_clusters: int):
        warnings.warn("plot_clusters() function haven't been tested yet")
        path_to_clusters_file = path_to_clusters_file.replace('\\', '/')
        folder_to_save = folder_to_save.replace('\\', '/')
        self.commands_to_run += '''
        path_outcomes <- paste(path_outcomes_folder, "/", "''' + outcome + '''",sep="")
        df_outcomes <- arrow::read_feather(path_outcomes)
        path_clusters <- "''' + path_to_clusters_file + '''"

        for (i in 1:''' + str(amount_of_clusters) + ''') {
            clusters_df_new <- read_feather(path_clusters)
            clusters_df_new$PIC[clusters_df_new$''' + clustering_method + ''' != i] <- 0
            clus_plot <- plot.timeseries.clustered(df_outcomes, clusters_df_new[, "''' + clustering_method + '''"])
            save_loc <- paste("''' + folder_to_save + '''/", "''' + clustering_method + '''","_", toString(i), ".png", sep="")
            ggsave(plot = clus_plot, save_loc, h = 8, w = 8, type = "cairo-png", dpi=300)
        }
        '''

    def save_clusters(self, savefile_path='./../Data/', save_with_date=False):
        savefile_path = savefile_path.replace('\\', '/')
        date_string = ''
        if save_with_date:
            date_string = ', data_date'
        self.commands_to_run += '''
        # export clustering solutions for rule induction in Python
        clustersolutions_name <- ''' + self.clustering_methods_to_perform[1:-1] + '''
        path_clusters <- paste(wd, "/''' + \
                                savefile_path + '", "/"' + date_string + ''', clustersolutions_name, ".feather", sep="")
        write_feather(df_cl3, path_clusters)
        '''
