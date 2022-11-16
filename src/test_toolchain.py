from ema_workbench import (
    TimeSeriesOutcome,
    perform_experiments,
    RealParameter,
    ema_logging,
)

from ema_workbench.connectors.vensim import VensimModel

import datamanager

# vensim = ctypes.windll.LoadLibrary(r'C:\Windows\System32\vendll64.dll')
# PATH_TO_MODEL = "/mnt/c/Users/lukac/PycharmProjects/SD_scenario_analysis/model/NL-Pandem-2-Cap_vensim_v_Sparkie.mdl"

ema_logging.log_to_stderr(ema_logging.INFO)

wd = r"G:\My Drive\Thesis\8_SRQ2\verifying Lisette's model\sandbox"
model_file_name = "Sparkies_playground.vpmx"

model = VensimModel("simpleModel", wd=wd, model_file=model_file_name)
# model = pysd.read_vensim(PATH_TO_MODEL)

model.uncertainties = [RealParameter("in rate", 0, 2.5), RealParameter("outrate", 0, 5)]

model.outcomes = [TimeSeriesOutcome('R')]

experiments, results = perform_experiments(model, 1)

deb = 0
# import matplotlib.pyplot as plt
# from ema_workbench.analysis.plotting import lines
#
# figure = lines(experiments, results, density=True) #show lines, and end state density
# plt.show()


# nr_experiments = 10
#     with MultiprocessingEvaluator(model) as evaluator:
#     results = perform_experiments(model, nr_experiments, evaluator=evaluator)
