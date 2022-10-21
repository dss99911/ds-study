import torch
import tensor

# tensor를 gpu메모리로 이동
if torch.cuda.is_available():
    tensor = tensor.to("cuda")

