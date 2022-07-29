import torch

# https://pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html
# https://pytorch.org/tutorials/beginner/pytorch_with_examples.html
#%% 피쳐, 레이블, 파라미터(w,b) 초기화
x = torch.ones(5)  # input tensor
y = torch.zeros(3)  # expected output
w = torch.randn(5, 3, requires_grad=True)
b = torch.randn(3, requires_grad=True)

#%% forward 계산 및 loss 구하기
z = torch.matmul(x, w)+b
loss = torch.nn.functional.binary_cross_entropy_with_logits(z, y)

#%%
print(f"Gradient function for z = {z.grad_fn}")
print(f"Gradient function for loss = {loss.grad_fn}")

#%% compute gradients. 미분값으로, w,b가 변경되어야할 기울기
print("w", w)
print("b", b)
optimizer = torch.optim.SGD([w, b], lr=1e-3)
optimizer.zero_grad()  # grad를 0으로 설정
loss.backward()  # gradient계산. forward()를 수행 후, 호출 가능
print("w.grad", w.grad)  # 처음엔 None이었다가, backward이후 값 생성
print("b.grad", b.grad)
optimizer.step()  # grad를 반영
print("w reflected", w)
print("b reflected", b)



#%% inference시 no_grad를 사용하여, grad 히스토리를 추적하지 않게 한다.
print(z.requires_grad)
with torch.no_grad():
    z = torch.matmul(x, w)+b
print(z.requires_grad)  # False


#%% parameter를 frozen시켜, pretrained network finetuing할 때도, no_grad를 적용한다.
z = torch.matmul(x, w)+b
z_det = z.detach()
print(z_det.requires_grad)  # False


#%% Jacobian Products
# retain_graph를 하면, backward를 여러번 가능
# grad자체가 미분값이면, backward를 두번하게 되면, 미분값만큼 값 이동을 두번한다는 의미 인듯
inp = torch.eye(5, requires_grad=True)
out = (inp+1).pow(2)
out.backward(torch.ones_like(inp), retain_graph=True)
print(f"First call\n{inp.grad}")
out.backward(torch.ones_like(inp), retain_graph=True)
print(f"\nSecond call\n{inp.grad}")
inp.grad.zero_()
out.backward(torch.ones_like(inp), retain_graph=True)
print(f"\nCall after zeroing gradients\n{inp.grad}")
