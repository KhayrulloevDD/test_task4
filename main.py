import pandas as pd
import timeit


def main():
    df = pd.read_pickle('contracts_data.pkl')
    pd.set_option('display.max_columns', 205)
    pd.set_option('display.max_rows', 5)

    products_df = df[['_regNum', 'products.product']]

    result = []

    for _, product in products_df.iterrows():
        index = 0
        for row in product['products.product']:
            index += 1
            new_row = {'_regNum': product['_regNum'], 'inner_index': index}
            for column in row:
                if isinstance(row[column], dict):
                    new_row = add_columns_from_dict(column, row[column], new_row)
                else:
                    new_row[column] = row[column]
            result.append(new_row)

    result_df = pd.DataFrame(result)

    print(result_df)


def add_columns_from_dict(column_name, column_value_dict, new_row):
    for key, value in column_value_dict.items():
        if isinstance(value, dict):
            new_row = add_columns_from_dict(f'{column_name}.{key}', column_value_dict[key], new_row)
        else:
            new_row[f'{column_name}.{key}'] = value
    return new_row


if __name__ == "__main__":
    start = timeit.default_timer()

    main()

    spent = timeit.default_timer() - start

    print(f'Время выполнения: {round(spent, 2)} секунд')
