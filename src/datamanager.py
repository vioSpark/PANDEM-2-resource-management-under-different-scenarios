import pyarrow.feather as feather
from tqdm import tqdm
from datetime import datetime
import pandas as pd
import logging
import os

from pickle import dump, load

log = logging.getLogger()


# As a general note: I don't know how to handle the R side nicely, so this DataManager class became an absolute hell
# I'd say priority 2 to refactor

class DataManager:
    def __init__(self, path_to_save_folder='../Data/', folder_name=None, saved_outcomes=None):
        now = datetime.now()
        if folder_name is None:
            folder_name = str(now.strftime("%Y_%m_%d"))
        if saved_outcomes is None:
            self.saved_outcomes = []
        else:
            self.saved_outcomes = saved_outcomes
        self.save_folder_path = os.path.join(path_to_save_folder, folder_name)
        self.experiments_file_name = 'experiments.feather'
        self.outcomes_file_name = 'outcomes.feather'
        self.plots_path = os.path.join(self.save_folder_path, 'plots')
        self.time_series_plots_path = os.path.join(self.plots_path, 'time_series')
        self.scatter_plots_path = os.path.join(self.plots_path, 'scatter')

        self.misc_data = os.path.join(self.save_folder_path, 'misc_data')
        os.makedirs(self.time_series_plots_path, exist_ok=True)
        os.makedirs(self.scatter_plots_path, exist_ok=True)
        os.makedirs(self.misc_data, exist_ok=True)

    def save_experiments(self, experiments, number_of_uncertainties=1):
        # TODO: use ema_workbench.util.utilities.save_results instead of feather
        log.info('saving experiments')
        save_path = os.path.join(self.save_folder_path, self.experiments_file_name)
        # +1 bc we also want to export the scenario column (run id-s)
        feather.write_feather(experiments.iloc[:, 0:number_of_uncertainties + 1], save_path)

    def save_outcomes(self, outcomes):
        # TODO: use ema_workbench.util.utilities.save_results instead of feather
        """
        takes EMA outcomes and exports all time series for each outcome of interest as a .feather dataframe for easy
        import into R. Arguments: export_outcomes(name of EMA outcomes dict, desired save location).
        Save location must exist
        """
        log.info('saving outcomes')
        outcomes_list = list(outcomes.keys())

        for outcome in tqdm(outcomes_list):
            df_temp = pd.DataFrame(outcomes[outcome])
            # df_temp = df_temp.copy()
            self.saved_outcomes.append(outcome)
            save_path = os.path.join(self.save_folder_path, outcome + '_' + self.outcomes_file_name)
            feather.write_feather(df_temp, save_path)
        dump(outcomes_list, open(os.path.join(self.save_folder_path, 'outcomes_list'), 'wb'))

    def load_outcomes(self, outcomes_to_load='all'):
        # TODO: use ema_workbench.util.utilities.save_results instead of feather
        """
        load previously generated outcomes with feather, and reshape to EMA style dictionary
        :return:
        """
        self.saved_outcomes = load(open(os.path.join(self.save_folder_path, 'outcomes_list'), 'rb'))
        outcomes = {}
        if outcomes_to_load == 'all':
            for outcome_id in tqdm(self.saved_outcomes):
                df_ts = feather.read_feather(
                    os.path.join(self.save_folder_path, outcome_id + '_' + self.outcomes_file_name))
                nd_ts = df_ts.values
                outcomes[outcome_id] = nd_ts
        else:
            if len(self.saved_outcomes) == 2:
                # ugly stuff to get the non 'TIME' variable from the list
                outcome_id = [i for i in self.saved_outcomes if i != 'TIME'][0]
                df_ts = feather.read_feather(
                    os.path.join(self.save_folder_path, outcome_id + '_' + self.outcomes_file_name))
                nd_ts = df_ts.values
                outcomes = {str(outcome_id): nd_ts}
            else:
                raise NotImplementedError()
            # outcome_id = outcome_to_load.replace(' ', '')

        return outcomes

    def load_experiments(self, model_name='Pandem2'):
        # TODO: use ema_workbench.util.utilities.save_results instead of feather
        """
        load previously generated experiments with feather
        :param model_name:
        :return:
        """
        df_experiments = feather.read_feather(os.path.join(self.save_folder_path, self.experiments_file_name))
        df_experiments['policy'] = 'None'
        df_experiments['model'] = model_name
        return df_experiments

    def get_save_folder_path(self):
        # maybe make a separate folder in the future
        return self.save_folder_path

    def get_outcomes_path(self, outcome_to_load=None):
        """
        load previously generated outcomes with feather, and reshape to EMA style dictionary
        :param outcome_to_load: In case of multiple outcomes specify which one to load.
        :return:
        """
        # self.saved_outcomes is 2 bc TIME is always going to be saved
        if outcome_to_load is None and len(self.saved_outcomes) == 2:
            outcome_id = next(iter(self.saved_outcomes))
            return os.path.join(self.save_folder_path, outcome_id + '_' + self.outcomes_file_name)

        if outcome_to_load is None:
            raise RuntimeError("There are more than one outcomes saved, automatic selection failed")

        # Do a UML diagram and refactor the datamanager class -> no time for that :/
        outcome_id = outcome_to_load
        return os.path.join(self.save_folder_path, outcome_id + '_' + self.outcomes_file_name)

    def get_experiments_path(self):
        return os.path.join(self.save_folder_path, self.experiments_file_name)

    def get_time_series_plots_path(self):
        return self.time_series_plots_path

    def get_misc_data_path(self):
        return self.misc_data

    def get_clusters_path(self, clustering_methods):
        file_name = "".join(method for method in clustering_methods)
        return os.path.join(self.save_folder_path, file_name + '.feather')

    def load_clusters(self, clustering_methods):
        df_clusters = feather.read_feather(self.get_clusters_path(clustering_methods))
        return df_clusters
