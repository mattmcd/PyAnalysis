# Data Science from Scratch hapter 3 
from matplotlib import pyplot as plt


# Example time series line chart
def exampleLineChart():
    years = [1950, 1960, 1970, 1980, 1990, 2000, 2010]
    gdp = [300.2, 543.5, 1075.9, 2862.5, 5979.6, 10289.7, 14958.3]

    # Line chart
    plt.plot(years, gdp, color='green', marker='o', linestyle='solid')
    plt.title("Nominal GDP")
    plt.ylabel("Billions of $")
    plt.show()

#Example bar chart
def exampleBarChart():
    movies = ['Annie Hall', 'Ben-Hur', 'Casablanca', 'Ghandi', 'West Side Story']
    num_oscars = [5,11,3,8,10]
    #Bar default width is 0.8 so add 0.1 to left coords to centre
    xs = [i + 0.1 for i,_ in enumerate(movies)]
    plt.bar(xs, num_oscars)
    plt.ylabel('# of Academy Awards')
    plt.title('My favourite movies')
    plt.xticks([i + 0.5 for i,_ in enumerate(movies)], movies)
    plt.show()

# Another example line chart
def exampleLineChartTrend():
    variance = [1,2,4,8,16,32,64,128,256]
    bias_squared = [256,128,64,32,16,8,4,2,1]
    total_error = [v+b for (v,b) in zip(variance,bias_squared)]
    xs = [i for i,_ in enumerate(bias_squared)]
    # Multiple calls to plot
    plt.plot( xs, variance, 'g-', label='variance')
    plt.plot( xs, bias_squared, 'r-.', label='bias^2')
    plt.plot( xs, total_error, 'b:', label='total error')
    plt.legend(loc=9) # top-center
    plt.xlabel('model complexity')
    plt.ylabel('The Bias-Variance Tradeoff')
    plt.show()
    
# Scatter plot
def exampleScatterPlot():
    friends = [70, 65, 72, 63, 71, 64, 60, 64, 67]
    minutes = [175, 170, 205, 120, 220, 130, 105, 145, 190]
    labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    plt.scatter(friends, minutes)
    for label, friend_count, minute_count in zip(labels, friends, minutes):
        plt.annotate(label, xy=(friend_count, minute_count), xytext=(5,-5), textcoords='offset points')
    plt.title('Daily minutes vs. Number of Friends')
    plt.xlabel('# of friends')
    plt.ylabel('daily minutes spent on site')
    plt.show()