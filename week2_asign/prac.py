def read_data(filename):
    # TODO) Read `filename` as a list of integer numbers
    with open(filename,'r') as fi:
        try:
            for line in fi.readlines():
                try:
                    data=[int(word) for word in line.split(',')]
                except ValueError as ex:
                    print(f'A line is ignored. (message:{ex})')
        except Exception as ex:
            print(f'Cannot run the program. (message: {ex})')
    return data
file_path = r"C:\Open-Source-Software\week2_asign\class_score_en.csv"
read_data(file_path)