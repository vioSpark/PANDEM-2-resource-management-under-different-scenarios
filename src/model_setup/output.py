import ema_workbench


class Outcomes:
    class Raw:
        infectious = [
            ema_workbench.TimeSeriesOutcome('I[g1, isolated]'),
            ema_workbench.TimeSeriesOutcome('I[g2, isolated]'),
            ema_workbench.TimeSeriesOutcome('I[g3, isolated]'),
            ema_workbench.TimeSeriesOutcome('I[g1, nonisolated]'),
            ema_workbench.TimeSeriesOutcome('I[g2, nonisolated]'),
            ema_workbench.TimeSeriesOutcome('I[g3, nonisolated]')
        ]

        infection = [
            ema_workbench.TimeSeriesOutcome('infection[g1, isolated]'),
            ema_workbench.TimeSeriesOutcome('infection[g2, isolated]'),
            ema_workbench.TimeSeriesOutcome('infection[g3, isolated]'),
            ema_workbench.TimeSeriesOutcome('infection[g1, nonisolated]'),
            ema_workbench.TimeSeriesOutcome('infection[g2, nonisolated]'),
            ema_workbench.TimeSeriesOutcome('infection[g3, nonisolated]')
        ]

        hospitalized_per_day = [
            ema_workbench.TimeSeriesOutcome('symptomatic hospitalized[g1, isolated]'),
            ema_workbench.TimeSeriesOutcome('symptomatic hospitalized[g2, isolated]'),
            ema_workbench.TimeSeriesOutcome('symptomatic hospitalized[g3, isolated]'),
            ema_workbench.TimeSeriesOutcome('symptomatic hospitalized[g1, nonisolated]'),
            ema_workbench.TimeSeriesOutcome('symptomatic hospitalized[g2, nonisolated]'),
            ema_workbench.TimeSeriesOutcome('symptomatic hospitalized[g3, nonisolated]')
        ]

        recovered = [
            ema_workbench.TimeSeriesOutcome('R[g1]'),
            ema_workbench.TimeSeriesOutcome('R[g2]'),
            ema_workbench.TimeSeriesOutcome('R[g3]')
        ]
        vaccination = [
            ema_workbench.TimeSeriesOutcome('vaccination[g1]'),
            ema_workbench.TimeSeriesOutcome('vaccination[g2]'),
            ema_workbench.TimeSeriesOutcome('vaccination[g3]')
        ]
        vaccinated = [
            ema_workbench.TimeSeriesOutcome('vaccinated[g1]'),
            ema_workbench.TimeSeriesOutcome('vaccinated[g2]'),
            ema_workbench.TimeSeriesOutcome('vaccinated[g3]')
        ]

        total_living = [
            ema_workbench.TimeSeriesOutcome('total number of living persons[g1]'),
            ema_workbench.TimeSeriesOutcome('total number of living persons[g2]'),
            ema_workbench.TimeSeriesOutcome('total number of living persons[g3]')
        ]

        deceased = [
            ema_workbench.TimeSeriesOutcome('deceased[g1]'),
            ema_workbench.TimeSeriesOutcome('deceased[g2]'),
            ema_workbench.TimeSeriesOutcome('deceased[g3]')
        ]

        # hospital
        ward_occupancy = [
            ema_workbench.TimeSeriesOutcome('ward[g1]'),
            ema_workbench.TimeSeriesOutcome('ward[g2]'),
            ema_workbench.TimeSeriesOutcome('ward[g3]')
        ]

        ward_capacity = [ema_workbench.TimeSeriesOutcome('ward capacity supply')]

        ICU_occupancy = [
            ema_workbench.TimeSeriesOutcome('ICU[g1]'),
            ema_workbench.TimeSeriesOutcome('ICU[g2]'),
            ema_workbench.TimeSeriesOutcome('ICU[g3]')
        ]

        ICU_capacity = [ema_workbench.TimeSeriesOutcome('ICU capacity supply')]

        ppe_usage = [ema_workbench.TimeSeriesOutcome('PPE usage')]
        ppe_stockpile = [ema_workbench.TimeSeriesOutcome('PPE')]

        # public health
        vaccinations = [ema_workbench.TimeSeriesOutcome('vaccinations')]

        test_usage = [ema_workbench.TimeSeriesOutcome('test use')]

        testing_rate = [
            ema_workbench.TimeSeriesOutcome('testing rate by age group[g1]'),
            ema_workbench.TimeSeriesOutcome('testing rate by age group[g2]'),
            ema_workbench.TimeSeriesOutcome('testing rate by age group[g3]')
        ]

        testing_demand = [
            ema_workbench.TimeSeriesOutcome('combined testing demand[g1]'),
            ema_workbench.TimeSeriesOutcome('combined testing demand[g2]'),
            ema_workbench.TimeSeriesOutcome('combined testing demand[g3]')
        ]

        testing_coverage = [
            ema_workbench.TimeSeriesOutcome('testing coverage[g1]'),
            ema_workbench.TimeSeriesOutcome('testing coverage[g2]'),
            ema_workbench.TimeSeriesOutcome('testing coverage[g3]'),
        ]

        contact_tracing_capacity = [ema_workbench.TimeSeriesOutcome('capacity for contact tracing per day')]

        contact_tracing_capacity_demand = [
            ema_workbench.TimeSeriesOutcome('tested unisolated symptomatics[g1]'),
            ema_workbench.TimeSeriesOutcome('tested unisolated symptomatics[g2]'),
            ema_workbench.TimeSeriesOutcome('tested unisolated symptomatics[g3]')
        ]


    other = Raw.ppe_usage + Raw.test_usage
    vaccination_related = Raw.vaccination + Raw.vaccinations
    testing_related = Raw.testing_rate + Raw.testing_coverage
    example_resources = other + Raw.ward_occupancy + Raw.ICU_occupancy
    ppt_tmp = Raw.infectious + Raw.ward_occupancy + Raw.ICU_occupancy + \
              Raw.deceased + vaccination_related + testing_related

    # Mart's list:
    # - Number of infected cases (per day)
    # - Number of infected cases that need hospitalization
    # - Number deceased
    mart_recommended_epi = Raw.infection + Raw.hospitalized_per_day + Raw.deceased
    # - number of ward beds needed / gap
    # - number of ICU beds needed / gap
    # - number of PPE needed / gap
    mart_recommended_hospital = Raw.ward_occupancy + Raw.ward_capacity + Raw.ICU_occupancy + \
                                Raw.ICU_capacity + Raw.ppe_usage + Raw.ppe_stockpile
    # - Testing capacity per day needed
    # - Contact tracing capacity per day needed
    mart_recommended_public_health = Raw.testing_demand + Raw.testing_rate + \
                                     Raw.contact_tracing_capacity + Raw.contact_tracing_capacity_demand
    mart_recommended = mart_recommended_epi + mart_recommended_hospital + mart_recommended_public_health
