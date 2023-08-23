import numpy as np
import matplotlib.pyplot as plt

n_groups = 7
resnet50_time = [1.1758601665496826, 0.3156430721282959, 0.24446463584899902, 0.2652163505554199, 0.24054408073425293, 0.196458101272583, 0.29340171813964844]
vgg_time = [0.7329444885253906, 0.6923706531524658, 0.2620553970336914, 0.3750300407409668, 0.34758543968200684, 0.2530391216278076, 0.5202255249023438]
xception_time = [1.4551944732666016, 0.4117703437805176, 0.28706860542297363, 0.3570594787597656, 0.35279083251953125, 0.2510795593261719, 0.323577880859375]

fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.2
opacity = 0.8

rects1 = plt.bar(index, resnet50_time, bar_width,
alpha=opacity,
color='b',
label='Resnet50')

rects2 = plt.bar(index + bar_width, vgg_time, bar_width,
alpha=opacity,
color='g',
label='VGG16')

rects3 = plt.bar(index + bar_width * 2, xception_time, bar_width,
alpha=opacity,
color='r',
label='Xception')

plt.xlabel('Query Number')
plt.ylabel('Time (s)')
plt.title('Time by Query Number')
plt.xticks(index + bar_width, ('1', '2', '3', '4', '5', '6', '7'))
plt.legend()

plt.tight_layout()
plt.savefig("Retrieval_time.png")
