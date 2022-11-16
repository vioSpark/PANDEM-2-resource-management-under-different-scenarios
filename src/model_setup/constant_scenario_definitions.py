import ema_workbench


class Constants:
    base_case = [
        ema_workbench.Constant('acquisition PPE', 9.0e+04),
        ema_workbench.Constant('test acqusition', 9.0e+03)
    ]

    intervention_0 = [
        ema_workbench.Constant('acquisition PPE', 9.0e+05)
    ]

    intervention_1 = [
        ema_workbench.Constant('test acqusition', 9.0e+04)
    ]

    intervention_2 = [
        ema_workbench.Constant('test acqusition', 9.0e+06),
        ema_workbench.Constant('testing staff', 2.0e+12)
    ]

    intervention_3 = [
        ema_workbench.Constant('LoS ward', 5.3)
    ]

    intervention_4 = [
        ema_workbench.Constant('staff visits per patient per day', 7.3),
        ema_workbench.Constant('"ICU patient-to-staff ratio"', 3)  # this should be in Lis's model, but it's not
    ]

    ICU_limit_lift = [
        ema_workbench.Constant('ICU bed capacity', 26000),
        ema_workbench.Constant('mechanical ventillator capacity', 100000),
    ]
    intervention_5 = [
        ema_workbench.Constant('staff visits per patient per day', 7.3),
        ema_workbench.Constant('ICU bed capacity', 26000),
        ema_workbench.Constant('mechanical ventillator capacity', 100000),
        ema_workbench.Constant('"ICU patient-to-staff ratio"', 3)  # this should be in Lis's model, but it's not
    ]

    interventions = [intervention_0, intervention_1, intervention_2, intervention_3, intervention_4,
                     intervention_5]
