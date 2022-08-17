import pandas as pd


def read_excel():
    """
    https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html
    """
    pd.read_excel("aa.xlsx")

def make_writer():
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    return pd.ExcelWriter('pandas_simple.xlsx',
                          engine='xlsxwriter',
                          datetime_format='mmm d yyyy hh:mm:ss',
                          date_format='mmmm dd yyyy',
                          options={'strings_to_urls': False})


def dataframe_to_writer(df=pd.DataFrame({'Data': [10, 20, 30, 20, 15, 30, 45]}), sheet_name='Sheet1'):
    writer = make_writer()

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name=sheet_name)
    return writer


def save_to_excel():
    # Close the Pandas Excel writer and output the Excel file.
    dataframe_to_writer().save()


def add_worksheet():
    writer = dataframe_to_writer()
    worksheet = writer.book.add_worksheet("new_sheet")
    writer.save()


def add_chart():
    sheet_name = 'Sheet1'
    writer = dataframe_to_writer(pd.DataFrame({'Data': [10, 20, 30, 20, 15, 30, 45]}), sheet_name)
    # Get the xlsxwriter objects from the dataframe writer object.
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    # Create a chart object.
    chart = workbook.add_chart({'type': 'column'})

    # Configure the series of the chart from the dataframe data.
    chart.add_series({'values': '=Sheet1!$B$2:$B$8'})

    # Insert the chart into the worksheet.
    worksheet.insert_chart('D2', chart)
    writer.save()


def cell_formatting():
    sheet_name = 'Sheet1'
    writer = dataframe_to_writer(pd.DataFrame({
        'Big Number': [100000, 201232, 3123210, 221340, 15, 30, 45],
        'Ratio': [0.1234, 20.213, 1, 0.9, 15, 30, 45]
    }), sheet_name)
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    # Add some cell formats.
    format1 = workbook.add_format({'num_format': '#,##0.00'})
    format2 = workbook.add_format({'num_format': '0%'})

    # Set the column width and format.
    # set_column should be added end of code. other code can change column width.
    worksheet.set_column('B:B', 18, format1)

    # Set the format but not the column width.
    worksheet.set_column('C:C', None, format2)
    writer.save()


def conditional_formatting():
    sheet_name = 'Sheet1'
    writer = dataframe_to_writer(pd.DataFrame({'Data': [10, 20, 30, 20, 15, 30, 45]}), sheet_name)
    worksheet = writer.sheets[sheet_name]
    worksheet.conditional_format('B2:B8', {'type': '3_color_scale'})
    writer.save()


def custom_header():
    # Turn off the default header and skip one row to allow us to insert a
    # user defined header.
    writer = make_writer()
    df = pd.DataFrame({'Data': [10, 20, 30, 20, 15, 30, 45]})

    # make empty row on 0 without header
    df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False)

    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    # Add a header format.
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#D7E4BC',
        'border': 1})

    # Write the column headers with the defined format.
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num + 1, value, header_format)
    writer.save()


def make_table():
    sheet_name = 'Sheet1'
    writer = make_writer()
    df = pd.DataFrame({
        'Big Number': [100000, 201232, 3123210, 221340, 15, 30, 45],
        'Ratio': [0.1234, 20.213, 1, 0.9, 15, 30, 45]
    })

    # make empty row on 0 without header
    # index false doesn't add first column for index
    df.to_excel(writer, sheet_name=sheet_name, startrow=1, header=False, index=False)
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    column_settings = [{'header': column} for column in df.columns]
    (max_row, max_col) = df.shape
    worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})

    writer.save()


def auto_filter():
    sheet_name = 'Sheet1'
    writer = make_writer()
    df = pd.DataFrame({
        'Big Number': [100000, 201232, 3123210, 221340, 15, 30, 45],
        'Ratio': [0.1234, 20.213, 1, 0.9, 15, 30, 45]
    })

    # make empty row on 0 without header
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    (max_row, max_col) = df.shape

    # set filter
    worksheet.autofilter(0, 0, max_row, max_col - 1)

    # apply specific filter on setting(but doesn't hide)
    worksheet.filter_column(1, 'Ratio >= 0.5')

    # hide row.
    for row_num in (df.index[(df['Ratio'] < 0.5)].tolist()):
        worksheet.set_row(row_num + 1, options={'hidden': True})

    writer.save()


def multiple_pandas():
    # Position the dataframes in the worksheet.
    df1 = pd.DataFrame({'Data': [10, 20, 30, 20, 15, 30, 45]})
    df2 = pd.DataFrame({'Data': [10, 20, 30, 20, 15, 30, 45]})
    df3 = pd.DataFrame({'Data': [10, 20, 30, 20, 15, 30, 45]})

    writer = make_writer()
    df1.to_excel(writer, sheet_name='Sheet1')  # Default position, cell A1.
    df1.to_excel(writer, sheet_name='Sheet2')
    df2.to_excel(writer, sheet_name='Sheet1', startcol=3)
    df3.to_excel(writer, sheet_name='Sheet1', startrow=6)

    writer.save()


def data_validation():
    """
    https://xlsxwriter.readthedocs.io/worksheet.html#worksheet-data-validation
    """
    sheet_name = 'Sheet1'
    writer = dataframe_to_writer(pd.DataFrame({'Data': [10, 20, 30, 20, 15, 30, 45]}), sheet_name)
    # Get the xlsxwriter objects from the dataframe writer object.
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    # integer validation(shows error popup when input)
    worksheet.data_validation('B3', {'validate': 'integer',
                                     'criteria': 'between',
                                     'minimum': 1,
                                     'maximum': 10})

    # List validation(shows dropdown list)
    worksheet.data_validation('B13', {'validate': 'list',
                                      'source': ['open', 'high', 'close']})

    # input cell
    # worksheet.data_validation(0, 0, 4, 1, {...})
    # worksheet.data_validation('B1',       {...})
    # worksheet.data_validation('C1:E5',    {...})

    writer.save()


def freeze_panes():
    writer = dataframe_to_writer()
    worksheet = writer.book.add_worksheet("new_sheet")
    # Freeze pane on the top row.
    worksheet.freeze_panes(1, 0)
    writer.save()


def fill_bg_color():
    writer = dataframe_to_writer()
    workbook = writer.book
    cell_format = workbook.add_format()
    cell_format.set_pattern(1)  # This is optional when using a solid fill.
    cell_format.set_bg_color('green')
    writer.save()


if __name__ == '__main__':
    data_validation()
