import ema_workbench
import pandas as pd


class Uncertainties:
    # 20-30 is okay for uncertainties (Willem)
    @staticmethod
    def no_uncertainty(tr=0.01875):
        return [ema_workbench.RealParameter("transmission probability", tr, tr * 1.000000001)]

    fake_PPE_acqusition_change = [
        ema_workbench.RealParameter("acquisition PPE", 2.5e+04, 2.5e+05)
    ]

    fake_test_acqusition_change = [
        ema_workbench.RealParameter("test acqusition", 9.0e+03, 9.0e+04)
    ]

    fake_LoS_ward_change = [
        ema_workbench.RealParameter("LoS ward", 5.3, 21.2)
    ]

    fake_ICU_patient_to_staff_ratio = [
        ema_workbench.RealParameter('staff visits per patient per day', 0.75, 3),
        ema_workbench.RealParameter('mechanical ventillator capacity', 100000, 100001),
        ema_workbench.RealParameter('ICU bed capacity', 26000, 260001)
    ]

    fake_ICU_staff_visits_per_patient_per_day = [
        ema_workbench.RealParameter('staff visits per patient per day', 5, 14.6),
        ema_workbench.RealParameter('"ICU patient-to-staff ratio"', 0.75, 3),
        ema_workbench.RealParameter('mechanical ventillator capacity', 10000, 10001),
        ema_workbench.RealParameter('ICU bed capacity', 26000, 26001),
        ema_workbench.RealParameter("acquisition PPE", 5e+04, 5.00001e+04)
    ]

    fake_ICU_staff_high = [
        ema_workbench.RealParameter('staff visits per patient per day', 14.5, 14.6),
        ema_workbench.RealParameter('"ICU patient-to-staff ratio"', 0.75, 0.75),
        ema_workbench.RealParameter('mechanical ventillator capacity', 10000, 10001),
        ema_workbench.RealParameter('ICU bed capacity', 26000, 26001),
        ema_workbench.RealParameter("acquisition PPE", 5e+04, 5.00001e+04)
    ]

    fake_ICU_staff_low = [
        ema_workbench.RealParameter('staff visits per patient per day', 5, 5.1),
        ema_workbench.RealParameter('"ICU patient-to-staff ratio"', 2.9, 3),
        ema_workbench.RealParameter('mechanical ventillator capacity', 10000, 10001),
        ema_workbench.RealParameter('ICU bed capacity', 26000, 26001),
        ema_workbench.RealParameter("acquisition PPE", 5e+04, 5.00001e+04)
    ]

    fake_tests_are_op = [
        ema_workbench.RealParameter("test acqusition", 9.0e+03, 9.0e+05),
        ema_workbench.RealParameter("testing staff", 1.0e+12, 2.0e+12)
    ]

    test_input = [
        ema_workbench.RealParameter("transmission probability", 0, 1),
        ema_workbench.RealParameter("incubation time", 1, 5),
        ema_workbench.RealParameter("waning immunity", 5 * 30, 10 * 30),
        ema_workbench.RealParameter("immunity period", 5 * 30, 10 * 30),
        ema_workbench.RealParameter("acquisition vaccinations", 50, 500),
        ema_workbench.RealParameter("incubation time", 2, 5),
        ema_workbench.RealParameter("acquisition PPE", 500, 2000),
        ema_workbench.RealParameter("medication acquisition", 0, 20000)
    ]

    tmp_sc1 = [
        # mild scenario, resources are enough always
        ema_workbench.RealParameter("transmission probability", 0.1, 0.11),
    ]

    tmp_sc2 = [
        # severe epi-parameters,
        # resources run out during first wave but 1st wave is so severe that no real 2nd wave happens
        ema_workbench.RealParameter("transmission probability", 1, 1),

    ]

    tmp_sc3 = [
        # sever resource parameters, 1st wave -> run out of stockpile, 2nd wave -> acquisition speed is too low
        ema_workbench.RealParameter("transmission probability", 0.8, 1),
        ema_workbench.RealParameter("testing staff", 2000, 2000),
        ema_workbench.RealParameter("test acqusition", 9e+13, 9e+13),
        ema_workbench.RealParameter("public health test stockpile", 1000000, 1000000),
        ema_workbench.RealParameter("ward absenteeism", 0.7, 0.7),
        ema_workbench.RealParameter("ICU absenteeism", 0.7, 0.7),
    ]

    unchanged = [ema_workbench.RealParameter("transmission probability", 0.01875, 0.0187500001)]

    @staticmethod
    def read_from_excel(path=r'G:\My Drive\Thesis\8_SRQ2\5_uncertainities\uncertainties to use.xlsx', sheet=0):
        df = pd.read_excel(path, sheet_name=sheet, header=0)
        df = df[['parameters to use as uncertainty', 'typical values to use min', 'typical values to use max']].dropna()
        list_of_uncertainties = []
        for index, row in df.iterrows():
            uncertainty = ema_workbench.RealParameter(row['parameters to use as uncertainty'],
                                                      row['typical values to use min'],
                                                      row['typical values to use max'])
            list_of_uncertainties.append(uncertainty)
        return list_of_uncertainties

# Public Health Resources:
