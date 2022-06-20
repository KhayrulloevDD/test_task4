import timeit

import pandas as pd


def main():
    df = pd.read_pickle('contracts_data.pkl')
    pd.set_option('display.max_columns', 205)
    pd.set_option('display.max_rows', 10)

    products_df = df[['_regNum', 'products.product']]

    result = []
    for product_id, product in products_df.iterrows():
        normalized_products = pd.json_normalize(products_df['products.product'][product_id])

        normalized_products.insert(0, 'index', '')

        normalized_products.insert(0, '_regNum', products_df['_regNum'][product_id])
        index = 0
        for _, row in normalized_products.iterrows():
            index += 1
            row['index'] = index
            result.append(row)

    result_df = pd.DataFrame(result)
    result_df = result_df.reset_index(drop=True)
    print(result_df)


if __name__ == "__main__":
    start = timeit.default_timer()

    main()

    spent = timeit.default_timer() - start

    print(f'Время выполнения (json_normalize): {round(spent, 2)} секунд')
