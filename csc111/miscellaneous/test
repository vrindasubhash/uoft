provinces = create_provinces()
populate_data('all_provinces_covid_data.csv', provinces)
BC = provinces['BC']
d1 = datetime.strptime('1/2/22', '%d/%m/%y')
d2 = datetime.strptime('16-05-2022', '%d-%m-%Y')
BC.get_avg_cases(d1)
#0.14163582755460252
BC.get_avg_cases(d2)
#0.15967324952012035
BC.num_cases_increased(d1, d2)
#False
BC.num_cases_increased(d2, d1)
#True
