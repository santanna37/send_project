import jwt

KEY = "luizfelipedemenezesbernardo_27.09.90/37"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjE5LCJleHAiOjE3NzU4NTk3OTd9.xS_Vr2-Zv3Xmr8o3vD3MRTKZlIGoo5yiy_t73vpDqqs"

try:
    payload = jwt.decode(token, KEY, algorithms=["HS256"])
    print("OK:", payload)
except Exception as e:
    print("ERRO:", e)