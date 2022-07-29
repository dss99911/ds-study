import torch
import numpy as np

# numpy array와 비슷하다고 보면됨
# gpu활용이나 automatic differentiation에 최적화
# 보통, numpy와 밑단 데이터 메모리 공유 가능
# grad_fn, grad를 가지고 있고, 계산 히스토리 추적 가능

#%% create tensor
# from list
data = [[1.0, 2.0],[3.0, 4.0]]
x_data = torch.tensor(data)

# from numpy array
# Changes in the NumPy array reflects in the tensor.
np_array = np.array(data)
x_np = torch.from_numpy(np_array)

# from tensor, same shape, 1 value
x_ones = torch.ones_like(x_data)
print(f"Ones Tensor: \n {x_ones} \n")

# from tensor, same shape, randome data
x_rand = torch.rand_like(x_data, dtype=torch.float)

# create by shape

shape = (2,3)
rand_tensor = torch.rand(shape)
ones_tensor = torch.ones(shape) # [1,1,1],[1,1,1]
zeros_tensor = torch.zeros(shape) # [0,0,0],[0,0,0]

#%% attribute
tensor = rand_tensor
print(f"Shape of tensor: {tensor.shape}")
print(f"Shape of tensor: {tensor.size()}")
print(f"Datatype of tensor: {tensor.dtype}")
print(f"Device tensor is stored on: {tensor.device}")

print(f"First row: {tensor[0]}")
print(f"First column: {tensor[:, 0]}")
print(f"Last column: {tensor[..., -1]}")
tensor[:,1] = 0
print(tensor)
print(tensor.view(tensor.size(1), -1))  # change shape

#%% join
tensor = torch.ones(4, 4, 4)
t0 = torch.cat([tensor, tensor, tensor], dim=0)  # (12, 4, 4) dimension
t1 = torch.cat([tensor, tensor, tensor], dim=1)  # (4, 12, 4)
t2 = torch.cat([tensor, tensor, tensor], dim=2)  # (4, 4, 12)
print(t1)


#%% operations

# matmul
# This computes the matrix multiplication between two tensors. y1, y2, y3 will have the same value
y1 = tensor @ tensor.T
y2 = tensor.matmul(tensor.T)

y3 = torch.rand_like(y1)
torch.matmul(tensor, tensor.T, out=y3)


# mul
# This computes the element-wise product. z1, z2, z3 will have the same value
z1 = tensor * tensor
z2 = tensor.mul(tensor)

z3 = torch.rand_like(tensor)
torch.mul(tensor, tensor, out=z3)

# sum
agg = tensor.sum()
agg_item = agg.item() # float
print(agg_item, type(agg_item))

# add
print(f"{tensor} \n")
tensor.add_(5) # inplace
print(tensor + 5) # create new tensor

# to numpy
# share the memory with numpy. so, if do tensor.add_(5), it's reflect to numpy as well
print(tensor.numpy())
