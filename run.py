from src.presentation.http_types.http_request import HttpRequest as http_request




http_request.body = {
  "full_name": "Sant Silva",
  "phone": "11999998888",
  "birth_date": "1998-05-12",
  "email": "sant@example.com",
  "themes": [
    "educacao",
    "igualdade racial",
    "politica"
  ],
  "address": "Rua da Empresa Feliz, 123 - São Paulo - 01010-010",
  "consent": True
}


# http_request2.body = {
#   "full_name": "sant Silva",
#   "phone": "11999998888",
#   "birth_date": "1998-05-12",
#   "email": "sant@example.com",
#   "themes": [
#     "educacao",
#     "igualdade racial",
#     "politica"
#   ],
#   "address": "Rua da Empresa Feliz, 123 - São Paulo - 01010-010",
#   "consent": True
# }

# http_request3.body = {
#   "full_name": "Sant da silva",
#   "phone": "11999998888",
#   "birth_date": "1998-05-12",
#   "email": "sant@example.com",
#   "themes": [
#     "educacao",
#     "igualdade racial",
#     "politica"
#   ],
#   "address": "Rua da Empresa Feliz, 123 - São Paulo - 01010-010",
#   "consent": True
# }



name = http_request

print(name.body['full_name'])