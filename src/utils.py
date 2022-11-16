import pandas as pd
import itertools


def convert_outcomes_to_df(outcomes):
    # construct df
    # df is a flattened 3D tensor > multiindex
    # columns   -> variable names (top level)
    # rows      -> [experiment_id, data_point_id]
    shape = outcomes['TIME'].shape
    index = pd.MultiIndex.from_product([range(shape[0]), range(shape[1])], names=['experiment_id', 'data_point_id'])
    df_outcomes = pd.DataFrame(columns=list(outcomes.keys()), index=index)
    # fill df with data
    for key, data_array in outcomes.items():
        flattened = data_array.flatten(order='C')
        df_outcomes[key] = flattened
    return df_outcomes



def convert_df_style_to_outcome(df_style_outcome):
    """
    convert a df-style outcome back to the shape EMA can interpret
    :param df_style_outcome:
    :return:
    """
    return df_style_outcome.unstack().values


def filter_dict(dictionary, keys):
    filtered = {key: dictionary[key] for key in keys}
    return filtered


def sum_over_subscript(df_outcomes, variable_name, subscript_type):
    """
    Sums over the outcomes for a subscripted vensim variable
    :param df_outcomes:
    :param variable_name: which variable to sum over
    :param subscript_type: 'age_group' or 'isolation_status' or 'both' for the respective summing / the product of it
    :return: another outcome in ema (dictionary) style
    """
    age_group = ['g1', 'g2', 'g3']
    isolation_status = ['isolated', 'nonisolated']

    if subscript_type == 'age_group':
        subscript = age_group
    elif subscript_type == 'isolation_status':
        subscript = isolation_status
    elif subscript_type == 'both' or subscript_type == 'all':
        both = itertools.product(age_group, isolation_status)
        subscript = []
        for item in both:
            subscript.append(item[0] + ', ' + item[1])
    else:
        raise RuntimeError('subscript {} is not in the pandem-2 model'.format(subscript_type))

    columns_to_sum = []
    for item in subscript:
        columns_to_sum.append(variable_name + '[' + item + ']')

    summed = df_outcomes[columns_to_sum].sum(axis=1)
    return convert_df_style_to_outcome(summed)
