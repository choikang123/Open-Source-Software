import matplotlib.pyplot as plt

def read_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            if not line.startswith('#'):  # If 'line' is not a header
                data.append([int(word) for word in line.split(',')])
    return data

if __name__ == '__main__':
    # Load score data
    class_kr = read_data('C:/Open-Source-Software/week4_assign/class_score_kr.csv')
    class_en = read_data('C:/Open-Source-Software/week4_assign/class_score_en.csv')
    
    # Prepare midterm, final, and total scores
    midterm_kr, final_kr = zip(*class_kr)  # unpacking to get midterm and final scores
    total_kr = [40/125 * midterm + 60/100 * final for (midterm, final) in class_kr]

    midterm_en, final_en = zip(*class_en)  # unpacking for English class
    total_en = [40/125 * midterm + 60/100 * final for (midterm, final) in class_en]  # Total scores for English class


    plt.figure(figsize=(10,5))
    plt.subplot(1, 2, 1) 

    # 스카터
    plt.scatter(midterm_kr, final_kr, color='red', label='Korean', marker='o')  
    plt.scatter(midterm_en, final_en, color='blue', label='English', marker='+')  
    plt.xlim(0, 125)  
    plt.ylim(0, 100)  
    plt.xlabel('Midterm Scores')  
    plt.ylabel('Final Scores')    
    plt.grid() 
    plt.legend() 
    plt.show() 
    
    # 히스토그램
    plt.figure(figsize=(8, 6))  
    plt.hist(total_kr, bins=range(0, 101, 5), color='red', alpha=0.7, label='Korean')
    plt.hist(total_en, bins=range(0, 101, 5), color='blue', alpha=0.5, label='English')
    
    plt.xlim(0, 100)  
    plt.xlabel('Total Scores')  
    plt.ylabel('The number of students')  
    plt.grid()  
    plt.legend() 

    plt.show()  