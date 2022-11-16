import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

import ema_workbench
from ema_workbench.connectors.vensim import VensimModel
from ema_workbench.analysis.prim import Prim

from datamanager import DataManager
import utils
from src.utils import convert_outcomes_to_df
from src.model_setup.input import Uncertainties
from src.model_setup.constant_scenario_definitions import Constants
from src.model_setup.output import Outcomes
from src import plots
from src.R_code_fragments import RInterface
import random

# log ema to stderr
ema_workbench.ema_logging.log_to_stderr(ema_workbench.ema_logging.INFO)


def run_experiments(uncertainties, model_outcomes, constants=None, data_manager: DataManager = None,
                    number_of_experiments: int = 1):
    working_directory = r"G:\My Drive\Thesis\8_SRQ2\4_reparamitrezation"
    vensim_model_file_name = "NL-Pandem-2-Cap_vensim_v_Sparkie_final.vpmx"

    model = VensimModel("Pandem2", wd=working_directory, model_file=vensim_model_file_name)
    model.uncertainties = uncertainties
    model.outcomes = model_outcomes
    model.constants = constants
    results = ema_workbench.perform_experiments(model, number_of_experiments)
    # with ema_workbench.MultiprocessingEvaluator(model) as evaluator:
    #     results = ema_workbench.perform_experiments(model, number_of_experiments, evaluator=evaluator)
    experiments, outcomes = results
    if data_manager is not None:
        data_manager.save_experiments(experiments, number_of_uncertainties=len(model.uncertainties))
        data_manager.save_outcomes(outcomes)
    return experiments, outcomes


def run_sc_style_experiments(intervention_constants, model_outcomes, three_way=False):
    working_directory = r"G:\My Drive\Thesis\8_SRQ2\4_reparamitrezation"
    vensim_model_file_name = "NL-Pandem-2-Cap_vensim_v_Sparkie_final.vpmx"

    model = VensimModel("Pandem2", wd=working_directory, model_file=vensim_model_file_name)
    model.uncertainties = Uncertainties.no_uncertainty()
    model.outcomes = model_outcomes

    # model_intervention = VensimModel("Pandem2", wd=working_directory, model_file=vensim_model_file_name)
    # model_intervention.outcomes = model_outcomes
    # model_intervention.constants = constants

    policies = [
        ema_workbench.Policy('base_case', constants=Constants.base_case),
        ema_workbench.Policy('intervention', constants=intervention_constants)
    ]
    if three_way:
        policies.insert(1, ema_workbench.Policy('ICU limits lifted', constants=Constants.ICU_limit_lift))

    return ema_workbench.perform_experiments(model, scenarios=1, policies=policies)


def main():
    program_flow_controls = {
        'run_experiments': True,
        'plot_results': True,
        'silhouette_calculation_and_plot': False,
        'cluster_calculation': False,
        'cluster_plotting': False,
        'PRIM': False
    }

    # experiments
    uncertainties = Uncertainties.fake_test_acqusition_change
    # uncertainties = Uncertainties.read_from_excel()
    outcomes = Outcomes.mart_recommended
    number_of_experiments = 2

    # silhouette_calculation_and_plot
    clustering_methods = ["PIC"]
    maximum_number_of_clusters_to_explore = 6

    # cluster_calculation
    clusters_to_create = 3

    if len(clustering_methods) != 1:
        raise NotImplementedError('Single run for more than 1 cluster is not supported yet')

    # Nice PRIM results here
    # data_manager = DataManager(path_to_save_folder='../Data', folder_name='08_08_2022')
    data_manager = DataManager(path_to_save_folder='../Data')

    # generate/load results
    if program_flow_controls['run_experiments']:
        experiments, outcomes = run_experiments(uncertainties, outcomes, data_manager, number_of_experiments)
    else:
        experiments = data_manager.load_experiments()
        outcomes = data_manager.load_outcomes()

    # post processing TODO: make this a function
    outcomes_df = convert_outcomes_to_df(outcomes)

    # old sum over subscripts

    # outcomes['I'] = utils.sum_over_subscript(outcomes_df, 'I', 'all')
    # outcomes['living'] = utils.sum_over_subscript(outcomes_df, 'total number of living persons', 'age_group')
    # outcomes['ward'] = utils.sum_over_subscript(outcomes_df, 'ward', 'age_group')
    # outcomes['ICU'] = utils.sum_over_subscript(outcomes_df, 'ICU', 'age_group')
    #
    # # calculate percentage
    # outcomes['percentage_infected'] = outcomes['I'] / outcomes['living']
    # outcomes['percentage_ward'] = outcomes['ward'] / outcomes['living']
    # outcomes['percentage_ICU'] = outcomes['ICU'] / outcomes['living']
    # outcomes['ward_to_capacity'] = outcomes['ward'] / 200000

    # add new 'columns' to outcomes_df
    outcomes_df = convert_outcomes_to_df(outcomes)

    # plot results
    if program_flow_controls['plot_results']:
        # plots.plot_experiments(experiments, outcomes, data_manager)

        exp_selector = slice(0, 1)

        # for time series
        # plots.plot_experiments(outcomes_df=outcomes_df, datamanager=data_manager,
        #                        outcome_selector=['PPE usage', 'PPE'], y_label_override=['PPE usage', 'PPE stockpile'],
        #                        experiment_selector=slice(0, 1))

        # experiments_to_select = slice(2, 3)
        # experiments_to_select = slice(13, 14)

        # plots.plot_experiments(experiments, outcomes, data_manager, outcomes_to_plot=['I'],
        #                        experiment_selector=experiments_to_select)
        # plots.plot_experiments(experiments, outcomes, data_manager, outcomes_to_plot=['ward'],
        #                        experiment_selector=experiments_to_select, code_black=200000)
        # plots.plot_experiments(experiments, outcomes, data_manager, outcomes_to_plot=['ICU'],
        #                        experiment_selector=experiments_to_select)
        # plots.plot_experiments(experiments, outcomes, data_manager, outcomes_to_plot=['PPE usage'],
        #                        experiment_selector=experiments_to_select)
        # plots.plot_experiments(experiments, outcomes, data_manager, outcomes_to_plot=['test use'],
        #                        experiment_selector=experiments_to_select, code_black=576000)

        # for percentage output
        # plots.plot_experiments(outcomes, data_manager, outcome_selector=['percentage_infected'],
        #                        experiment_selector=experiments_to_select)
        # plots.plot_experiments(outcomes, data_manager, outcome_selector=['percentage_ward'],
        #                        experiment_selector=experiments_to_select)
        # plots.plot_experiments(outcomes, data_manager, outcome_selector=['ward_to_capacity'],
        #                        experiment_selector=experiments_to_select)
        #
        # # scatter
        # scatter(experiments, outcomes, outcome_selector=['test use', 'ICU'],
        #         datamanager=data_manager, experiments_to_show=experiments_to_select)
        # scatter(experiments, outcomes, outcome_selector=['ward', 'ICU'],
        #         datamanager=data_manager, experiments_to_show=experiments_to_select)

    r = RInterface(data_manager.save_folder_path, data_manager.get_experiments_path(), clustering_methods)

    if program_flow_controls['silhouette_calculation_and_plot']:
        # todo: from silhouette data select the argmax() one, as s()=1 means that the clustering solution is perfect
        #  also give the user a warning if that value is below a threshold
        #  (let's say 0.8, but would need to look at the original article for some better  ideas )
        #  source:    file:///C:/Users/lukac/Downloads/20180827_MScThesis_Psteinmann.pdf
        if maximum_number_of_clusters_to_explore >= number_of_experiments:
            raise ValueError(
                "Not enough experiments: You need at least {} experiments to cluster into {} groups".format(
                    maximum_number_of_clusters_to_explore + 1, maximum_number_of_clusters_to_explore))

        r.calculate_and_plot_silhouettes(outcome="I[g1, isolated]_outcomes.feather",
                                         maximum_cluster_count=maximum_number_of_clusters_to_explore,
                                         plot_save_path=data_manager.plots_path + '/silhouettes.png',
                                         data_save_path=data_manager.get_misc_data_path() + '/silhouettes.feather')
        r.run()

        img = mpimg.imread(data_manager.plots_path + '/silhouettes.png')
        imgplot = plt.imshow(img)
        plt.axis('off')
        plt.show()

    if program_flow_controls['cluster_calculation']:
        # TODO: make this multi-threaded (hopefully within R)
        r.make_clusters('I[g1, isolated]_outcomes.feather', clusters_to_create)
        r.save_clusters(savefile_path=data_manager.get_save_folder_path())
        r.run()

    clusters_df = data_manager.load_clusters(clustering_methods)

    if program_flow_controls['cluster_plotting']:
        r.plot_clusters(outcome='I[g1, isolated]_outcomes.feather',
                        path_to_clusters_file=data_manager.get_clusters_path(clustering_methods),
                        folder_to_save=data_manager.plots_path, clustering_method='PIC',
                        amount_of_clusters=clusters_to_create)
        r.run()
        for i in range(clusters_to_create):
            img = mpimg.imread(data_manager.plots_path + '\\PIC_' + str(i + 1) + '.png')
            imgplot = plt.imshow(img)
            plt.axis('off')
            plt.show()

    if program_flow_controls['PRIM']:
        if len(clustering_methods) != 1: raise NotImplementedError
        cluster_column_name = clustering_methods[0]
        independent_variable = experiments
        num_of_clusters = clusters_df.max()[0]
        for cluster_number in range(1, num_of_clusters + 1):
            # https://numpy.org/doc/stable/reference/generated/numpy.where.html
            dependent_variable = np.where(clusters_df[cluster_column_name] == cluster_number, 1, 0)
            # Optional task: go back to GitHub issue, and figure out what happened
            threshold = 1 / num_of_clusters
            prim = Prim(x=independent_variable, y=dependent_variable, threshold=threshold, peel_alpha=0.05,
                        paste_alpha=0.05)

            box = prim.find_box()
            box.show_tradeoff()
            plt.show()

            # TODO: PRIM shenanigans??
            # selected_box = None  # automatically use last box

            box.inspect()
            box.inspect(style='graph')
            # box.select(selected_box)
            box.show_pairs_scatter()
            # if really needed the matplotlib axes size could be changed, but that's hacky
            # fig.set_size_inches((8, 8))
            plt.show()
            # TODO: save the plots
    # manually copy rules for box of choice into R ->
    # todo: only plotting happens there, make that happen here (aka end the nightmare....)
    r.run()


def plots_for_ws_ppt():
    outcomes = Outcomes.mart_recommended
    intervention_names = ['Increased PPE acquisition', 'Increased test acquisition', 'Unlimited tests',
                          'Reduced ward LoS', 'Reduced visit per patient', 'Limits lifted + Reduced visit', '???']

    selector = 5

    random.seed(69420912)
    np.random.seed(69420912)

    constants = Constants.interventions[selector]
    results = run_sc_style_experiments(constants, outcomes, three_way=selector == 5)

    # post-processing
    experiment, outcomes = results
    outcomes_df = calculate_gaps(outcomes)
    print(experiment.iloc[:, :])

    # plot results
    exp_selector = slice(0, 1)
    if selector == 5: exp_selector = slice(0, 2)

    # epi
    def legend_override(legend: str, selector):
        res = []
        if selector != 5:
            override = ['Baseline', intervention_names[selector]]
            for i in range(2):
                res.append(legend + ' - ' + override[i])
        else:
            override = ['Baseline', 'ICU limits lifted', intervention_names[selector]]
            for i in range(3):
                res.append(legend + ' - ' + override[i])
        return res

    def plot_experiments():
        plots.plot_experiments(outcomes_df=outcomes_df,
                               outcome_selector=['Infected cases (per day)'],
                               legend_override=legend_override('Infected cases', selector),
                               experiment_selector=exp_selector, y_units='person / day',
                               add_scenario_count=False)

        # if selector == 1:
        #     plots.plot_experiments(outcomes_df=outcomes_df,
        #                            outcome_selector=['infected isolated'],
        #                            legend_override=legend_override('Infected isolated cases'),
        #                            experiment_selector=exp_selector, y_units='person / day',
        #                            add_scenario_count=False)

        plots.plot_experiments(outcomes_df=outcomes_df,
                               outcome_selector=['Hospitalization (per day)'],
                               legend_override=legend_override('Hospitalization', selector),
                               experiment_selector=exp_selector, y_units='person / day',
                               add_scenario_count=False)

        plots.plot_experiments(outcomes_df=outcomes_df,
                               outcome_selector=['Deceased (total)'],
                               legend_override=legend_override('Deceased (total)', selector),
                               experiment_selector=exp_selector, y_units='person',
                               add_scenario_count=False)

        # hospital
        plots.plot_experiments(outcomes_df=outcomes_df,
                               outcome_selector=['ward beds gap'],
                               legend_override=legend_override('ward beds gap', selector),
                               experiment_selector=exp_selector, y_units='bed',
                               add_scenario_count=False)

        plots.plot_experiments(outcomes_df=outcomes_df,
                               outcome_selector=['ICU beds gap'],
                               legend_override=legend_override('ICU beds gap', selector),
                               experiment_selector=exp_selector, y_units='bed',
                               add_scenario_count=False)

        plots.plot_experiments(outcomes_df=outcomes_df,
                               outcome_selector=['PPE gap'],
                               legend_override=legend_override('PPE gap', selector),
                               experiment_selector=exp_selector, y_units='PPE kit',
                               add_scenario_count=False)

        # public health
        plots.plot_experiments(outcomes_df=outcomes_df,
                               outcome_selector=['testing gap'],
                               legend_override=legend_override('testing gap', selector),
                               experiment_selector=exp_selector, y_units='tests missing/day',
                               add_scenario_count=False)

        plots.plot_experiments(outcomes_df=outcomes_df,
                               outcome_selector=['contact tracing gap'],
                               legend_override=legend_override('contact tracing gap', selector),
                               experiment_selector=exp_selector, y_units="person couldn't be traced/day",
                               add_scenario_count=False)

    def plot_bars():
        plots.plot_bar(outcomes_df=outcomes_df,
                       outcome_selector=['Infected cases (per day)'],
                       legend_override=legend_override('Infected cases', selector),
                       experiment_selector=exp_selector, y_units='person / week',
                       add_scenario_count=False)

        plots.plot_bar(outcomes_df=outcomes_df,
                       outcome_selector=['Hospitalization (per day)'],
                       legend_override=legend_override('Hospitalization', selector),
                       experiment_selector=exp_selector, y_units='person / week',
                       add_scenario_count=False)

        plots.plot_bar(outcomes_df=outcomes_df,
                       outcome_selector=['Deceased (total)'],
                       legend_override=legend_override('Deceased (total)', selector),
                       experiment_selector=exp_selector, y_units='person',
                       add_scenario_count=False)

        # hospital
        plots.plot_bar(outcomes_df=outcomes_df,
                       outcome_selector=['ward beds gap'],
                       legend_override=legend_override('ward beds gap', selector),
                       experiment_selector=exp_selector, y_units='bed',
                       add_scenario_count=False)

        plots.plot_bar(outcomes_df=outcomes_df,
                       outcome_selector=['ICU beds gap'],
                       legend_override=legend_override('ICU beds gap', selector),
                       experiment_selector=exp_selector, y_units='bed',
                       add_scenario_count=False)

        plots.plot_bar(outcomes_df=outcomes_df,
                       outcome_selector=['PPE gap'],
                       legend_override=legend_override('PPE gap', selector),
                       experiment_selector=exp_selector, y_units='PPE kit',
                       add_scenario_count=False)

        # public health
        plots.plot_bar(outcomes_df=outcomes_df,
                       outcome_selector=['testing gap'],
                       legend_override=legend_override('testing gap', selector),
                       experiment_selector=exp_selector, y_units='tests missing/week',
                       add_scenario_count=False)

        plots.plot_bar(outcomes_df=outcomes_df,
                       outcome_selector=['contact tracing gap'],
                       legend_override=legend_override('contact tracing gap', selector),
                       experiment_selector=exp_selector, y_units="person couldn't be traced/week",
                       add_scenario_count=False)

    plot_experiments()
    plot_bars()


def calculate_gaps(outcomes):
    outcomes_df = convert_outcomes_to_df(outcomes)
    outcomes['Infected cases (per day)'] = utils.sum_over_subscript(outcomes_df, 'infection', 'all')
    # - Number of infected cases that need hospitalization
    outcomes['Hospitalization (per day)'] = utils.sum_over_subscript(outcomes_df, 'symptomatic hospitalized', 'all')
    # - Number deceased
    outcomes['Deceased (total)'] = utils.sum_over_subscript(outcomes_df, 'deceased', 'age_group')
    # hospital
    # - number of ward beds needed / gap + total ward beds occupied (double axes)
    outcomes['occupied ward beds'] = utils.sum_over_subscript(outcomes_df, 'ward', 'age_group')
    outcomes['ward beds gap'] = outcomes['occupied ward beds'] - outcomes['ward capacity supply']
    # - number of ICU beds needed / gap + total ICU beds occupied (double axis)
    outcomes['occupied ICU beds'] = utils.sum_over_subscript(outcomes_df, 'ICU', 'age_group')
    outcomes['ICU beds gap'] = outcomes['occupied ICU beds'] - outcomes['ICU capacity supply']
    # - number of PPE needed / gap
    outcomes['PPE gap'] = outcomes['PPE usage'] - outcomes['PPE']
    # - Testing capacity per day needed
    outcomes['testing demand'] = utils.sum_over_subscript(outcomes_df, 'combined testing demand', 'age_group')
    outcomes['testing rate'] = utils.sum_over_subscript(outcomes_df, 'testing rate by age group', 'age_group')
    outcomes['testing gap'] = outcomes['testing demand'] - outcomes['testing rate']
    # - Contact tracing capacity per day needed
    outcomes['contact tracing demand'] = utils.sum_over_subscript(outcomes_df, 'tested unisolated symptomatics',
                                                                  'age_group')
    outcomes['contact tracing gap'] = outcomes['contact tracing demand'] - outcomes[
        'capacity for contact tracing per day']
    # outcomes['infected isolated'] = utils.sum_over_subscript(outcomes_df, 'infection', 'age_group')
    outcomes_df = convert_outcomes_to_df(outcomes)
    return outcomes_df


plots_for_ws_ppt()
exit()
main()
