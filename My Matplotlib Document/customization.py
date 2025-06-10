import numpy as np
import matplotlib.pyplot as plt

# years = [2014,2015,2016,2017,
#          2018,2019,2020,2021]

# income = [55,56,62,61,
#           72,72,73,75]

# income_ticks = list(range(50,81,2))

# plt.plot(years,income)
# plt.title('Income of Lingga (USD)', fontsize=20, fontname='Comic Sans MS')
# plt.xlabel('Year')
# plt.ylabel('Yearly Income')
# plt.yticks(income_ticks, [f"${x}k" for x in income_ticks])
# plt.show()

stock_a = [100,102,99,101,101,100,102]
stock_b = [90,95,102,104,105,103,109]
stock_c = [110,115,100,105,100,98,95]

plt.plot(stock_a, label='Company1')
plt.plot(stock_b, label='Company2')
plt.plot(stock_c, label='Company3')
plt.legend(loc='upper center')

plt.show()