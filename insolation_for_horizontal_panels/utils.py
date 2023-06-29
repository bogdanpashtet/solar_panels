def write_data_hourly(writer, data):
    writer.writerow(
        ['hour_num', 'month_1', 'month_2', 'month_3', 'month_4', 'month_5', 'month_6', 'month_7', 'month_8', 'month_9',
         'month_10', 'month_11', 'month_12'])

    for i in data:
        writer.writerow(
            [i["hour_num"], i["month_1"], i["month_2"], i["month_3"], i["month_4"], i["month_5"], i["month_6"],
             i["month_7"], i["month_8"], i["month_9"], i["month_10"], i["month_11"], i["month_12"]])
