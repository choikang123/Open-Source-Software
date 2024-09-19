def read_data(filename):
    # TODO) Read `filename` as a list of integer numbers
    data = []  # 데이터 리스트 초기화
    with open(filename, 'r') as fi:
        try:
            for line in fi.readlines():  # [[ , ], [ , ], [ , ]]
                try:
                    # '#'로 시작하는 주석 라인은 무시
                    if line.startswith('#'):
                        continue
                    # 줄에서 정수로 변환된 데이터를 리스트에 추가
                    data.append([int(word) for word in line.split(',')])
                except ValueError as ex:
                    print(f'A line is ignored. (message: {ex})')
        except Exception as ex:
            print(f'Cannot run the program. (message: {ex})')
    return data  # 데이터 리스트 반환

file_path = r"C:\Open-Source-Software\week2_asign\class_score_en.csv"
data = read_data(file_path)

def calc_weighted_average(data_2d, weight):
    # TODO) Calculate the weighted averages of each row of `data_2d`
    average = []
    for data in data_2d:
        avg = weight[0] * data[0] + weight[1] * data[1]
        average.append(avg)
    return average

def analyze_data(data_1d):  # data_1d에는 리스트가 들어가 있다
    # TODO) Derive summary of the given `data_1d`
    n = len(data_1d)
    if n > 0:
        mean = sum(data_1d) / n
        sum2 = sum([datum**2 for datum in data_1d])
        var = sum2 / n - mean**2

        sorted_data = sorted(data_1d)
        if n % 2 == 1:
            median = sorted_data[n // 2]
        else:
            median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2        

        return mean, var, median, min(data_1d), max(data_1d)
    
    return 0, 0, 0, None, None

if __name__ == '__main__':
    data = read_data(file_path)
    if data and len(data[0]) == 2:  # Check 'data' is valid
        average = calc_weighted_average(data, [40 / 125, 60 / 100])

        # Write the analysis report as a markdown file
        with open('class_score_analysis.md', 'w') as report:
            report.write('### Individual Score\n\n')
            report.write('| Midterm | Final | Average |\n')
            report.write('| ------- | ----- | ----- |\n')
            for ((m_score, f_score), a_score) in zip(data, average):
                report.write(f'| {m_score} | {f_score} | {a_score:.3f} |\n')
            report.write('\n\n\n')

            report.write('### Examination Analysis\n')
            data_columns = {
                'Midterm': [m_score for m_score, _ in data],
                'Final': [f_score for _, f_score in data],
                'Average': average
            }
            for name, column in data_columns.items():
                mean, var, median, min_, max_ = analyze_data(column)
                report.write(f'* {name}\n')
                report.write(f'  * Mean: **{mean:.3f}**\n')
                report.write(f'  * Variance: {var:.3f}\n')
                report.write(f'  * Median: **{median:.3f}**\n')
                report.write(f'  * Min/Max: ({min_:.3f}, {max_:.3f})\n')
