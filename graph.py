import pymysql.cursors
import re
import plotly.express as px
import pandas as pd

engine_sizes = ['Up to 499cc', '500cc to 749cc', '750cc to 999cc', '1000cc to 1099cc', '1100cc to 1199cc', '1200cc to 1299cc', '1300cc to 1399cc', '1400cc to 1499cc', '1500cc to 1599cc', '1600cc to 1699cc', '1700cc to 1799cc', '1800cc to 1899cc', '1900cc to 1999cc', '2000cc to 2099cc', '2100cc to 2199cc', '2200cc to 2299cc', '2300cc to 2399cc', '2400cc to 2499cc', '2500cc to 2599cc', '2600cc to 2699cc', '2700cc to 2799cc', '2800cc to 2899cc', '2900cc to 2999cc', '3000cc to 3099cc', '3100cc to 3199cc', '3200cc to 3299cc', '3300cc to 3399cc', '3400cc to 3499cc', '3500cc to 3599cc', '3600cc to 3699cc', '3700cc to 3799cc', '3800cc to 3899cc', '3900cc to 3999cc', '4000cc to 4249cc', '4250cc to 4499cc', '4500cc to 4749cc', '4750cc to 4999cc', '5000cc to 5249cc', '5250cc to 5499cc', '5500cc to 5749cc', '5750cc to 5999cc', '6000cc to 6249cc', '6250cc to 6499cc', '6500cc to 6749cc', '6750cc to 6999cc', '7000cc to 7499cc', '7500cc to 7999cc', '8000cc to 8499cc', '8500cc to 8999cc', '9000cc to 9499cc', '9500cc to 9999cc', '10000cc and over']

ranges = {}
for range in engine_sizes:
    if re.match(r'Up to', range):
        ranges[range] = [0, int(re.match(r'Up to ([0-9]+)cc', range).group(1))]
    elif re.match(r'([0-9]+)cc and over', range):
        ranges[range] = [int(re.match(r'([0-9]+)cc and over', range).group(1)), 100000]
    else:
        match = re.match(r'([0-9]+)cc to ([0-9]+)cc', range)
        ranges[range] = [int(match.group(1)), int(match.group(2))]


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='password',
                             db='vehicle_emissions',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()
results = {}
total = 0
cursor.execute("SELECT * FROM cars INNER JOIN car_counts ON car_counts.car_id = cars.id;")
for row in cursor.fetchall():
    for size in engine_sizes:
        if row[size] != None:


# counts = []
# for key, value in results.items():
#     if key == None:
#         continue
#     counts += [key] * int(value / 1000)
# print(len(counts))
# import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt
#
# sns.set(style="white", palette="muted", color_codes=True)
#
# # Set up the matplotlib figure
# f, axes = plt.subplots(1, 1, figsize=(7, 7), sharex=True)
# sns.despine(left=True)
#
# # Plot a historgram and kernel density estimate
# sns.kdeplot(counts, color="m", bw=.5, ax=axes, shade=True)
#
# plt.axvline(2020, color='red')
# plt.axvline(2007, color='red')
# plt.setp(axes, yticks=[])
# plt.tight_layout()
# plt.show()
