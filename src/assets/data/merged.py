import csv

# 文件路径
income_file = 'src/assets/data/income.csv'
divorce_file = 'src/assets/data/divorce_rate.csv'
population_file = 'src/assets/data/population.csv'
output_file = 'src/assets/data/merged.csv'

# 读取csv为dict: {province: {year: value}}
def read_csv(file):
    with open(file, encoding='gbk') as f:  # 修改为 gbk
        reader = csv.reader(f)
        rows = list(reader)
        header = rows[0][1:]  # 跳过“地区”
        data = {}
        for row in rows[1:]:
            province = row[0]
            data[province] = {}
            for i, year in enumerate(header):
                data[province][year.replace('年','')] = row[i+1] if i+1 < len(row) else ''
        return data, [h.replace('年','') for h in header]

income_data, years = read_csv(income_file)
divorce_data, _ = read_csv(divorce_file)
population_data, _ = read_csv(population_file)

provinces = income_data.keys()

with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['year','province','income','divorce_rate','population'])
    for year in years:
        for province in provinces:
            income = income_data[province].get(year, '')
            divorce = divorce_data.get(province, {}).get(year, '')
            population = population_data.get(province, {}).get(year, '')
            writer.writerow([year, province, income, divorce, population])

print('合并完成，输出到', output_file)