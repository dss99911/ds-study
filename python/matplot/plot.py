import matplotlib.pyplot as plt
import numpy as np

#%% x, y

# x좌표 array,  y 좌표 array
# (1,1), (2,4), (3,2), (4,3) 의 좌표를 선으로 연결.
plt.plot([1, 2, 3, 4], [1, 4, 2, 3])
plt.plot([1, 4, 2, 3])  # y축만 있으면, x축은 index값으로 보여준다(0,1,2,3)
plt.plot([1, 2, 3, 4], [1, 4, 2, 3], [1, 2, 3, 4], [2, 5, 2, 3]) # 두개의 선을 그린다.
plt.plot([1, 2, 3, 4], [1, 4, 2, 3], "ro", [1, 2, 3, 4], [2, 5, 2, 3], "b^-") # 두개의 선을 그린다.
plt.plot([1, 2, 3, 4], ["apple", "b", "c", "d"]) # 숫자가 아닌 텍스트도 가능
plt.show()