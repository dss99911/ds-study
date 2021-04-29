import os
from os import listdir, path
from os.path import isfile, join

import pandas as pd

# Usage
# - set {dir} for parquet file's folder
# - configure column width by {data_columns_width}
# - configure queries and data validation by {query_columns}
# - it create folder f"{dir}-excel" and create excel files in it.
# - as parquet file is saved on each partition folder, in order to make single files in a directory,
#   - recommend to use copySingleFileOfPartitionToOutside

dir = "./directory"
data_columns_width = [16, 100, 10, 17]
query_columns = [
    ("Query1", {'validate': 'list', 'source': ['Y', 'N', "Related"]}, 12),
    ("Period", {'validate': 'list',
                'source': ['Non Periodic', '1d', '2d', '3d', '4d', '5d', '6d', '1w', '2w', '3w', '1m', '2m', '3m', '1y',
                           'etc']}, 10),
    ("Amount", {'validate': 'list', 'source': ['Fixed', 'Variable']}, 10),
    ("Necessary", {'validate': 'list', 'source': ['Y', 'N']}, 10),
    ("Category",
     {'validate': 'list', 'source':
         ['A', 'B']}, 12),
    ("Comment", None, 20),
]


def create_excel_file(parquet_path: str, excel_path: str):
    df = pd.read_parquet(parquet_path)
    writer = pd.ExcelWriter(excel_path,
                            engine='xlsxwriter',
                            datetime_format='yyyy-mm-dd hh:mm:ss',
                            date_format='yyyy-mm-dd',
                            options={'strings_to_urls': False})
    sheet_name = 'Sheet1'

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name=sheet_name, index=False)

    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    (max_row, max_col) = df.shape

    add_queries(workbook, worksheet, max_col, max_row)
    set_column_width(worksheet)
    worksheet.freeze_panes(1, 0)
    writer.save()


def add_queries(workbook, worksheet, max_col, max_row):
    for index in range(len(query_columns)):
        c = query_columns[index]
        col_index = max_col + index
        cell_format = workbook.add_format()
        cell_format.set_pattern(1)  # This is optional when using a solid fill.
        cell_format.set_bg_color('yellow')
        worksheet.write(0, col_index, c[0], cell_format)
        worksheet.set_column(col_index, col_index, query_columns[index][2])

        if c[1] is not None:
            worksheet.data_validation(1, col_index, max_row, col_index, c[1])

def set_column_width(worksheet):
    # for index in range(len(query_columns)):
    #     worksheet.set_column(index, index, query_columns[index][2])
    for index in range(len(data_columns_width)):
        worksheet.set_column(index, index, data_columns_width[index])


def list_files_name(path):
    return [f for f in listdir(path) if isfile(join(path, f))]


def list_files_path(path: str):
    return list(map(lambda x: f"{path.rstrip('/')}/{x}", list_files_name(path)))


if __name__ == '__main__':
    input_dir = dir.rstrip('/')
    output_dir = f"{input_dir}-excel"
    if not path.exists(output_dir):
        os.mkdir(output_dir)

    for f in list_files_name(input_dir):
        print("file: " + f)
        parquet_path = f"{input_dir}/{f}"
        excel_path = f"{output_dir}/{f.rstrip('.parquet')}.xlsx"
        create_excel_file(parquet_path, excel_path)
