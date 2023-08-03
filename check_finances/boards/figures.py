import matplotlib.pyplot as plt
from .models import Post



fig, ax = plt.subplots()
result = Post.objects.raw('select date, SUM(`sum`) as `sum` from boards_post GROUP by date')
date_x = []
sum_y = []

for i in result:
    date_x.append(i.date)
    sum_y.append(i.sum)


counts = [40, 100, 30, 55]
bar_labels = ['red', 'blue', '_red', 'orange']
bar_colors = ['tab:red', 'tab:blue', 'tab:red', 'tab:orange']

ax.bar(date_x, sum_y)

ax.set_ylabel('Sum')
ax.set_title('Sum by day')
#ax.legend(title='Fruit color')

plt.show()