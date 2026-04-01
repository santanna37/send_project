from typing import Dict
import unicodedata


class PersonValidator:

    def name_validator(self, name: str) -> str:
        """Validação de nome """
        name_str = name

        name_lista = name.split()
        novo = []
        name_person = ""
        # 1 - se não tiver nome
        if not name:
            raise ValueError("Nome é obrigatório")

        # 2 - se não tiver sobrenome
        if len(name_lista) <2:
            raise ValueError("Nome Completo Obrigatório")

        # 3 - se o nome tiver caracter invalido
        name_str = name_str.replace(' ','')
        for string in name_str:
            if not string.isalpha():
                raise ValueError('Nome contem números')
            
        # arrumar nome para DB
        for word in name_lista:
            if len(word) > 2:
                novo.append(word.capitalize())
            else:
                novo.append(word.lower())
            
            name_person = ' '.join(novo).strip()
    
        return name_person
    

    def email_validador(self, email_person: str) -> str:
        """ validador de email """

        email = email_person

        # tratamento de segurança
        email = unicodedata.normalize("NFKC", email)

        # 0 - tipo str para o email
        if not isinstance(email, str):
            raise ValueError("Email inválido")

        # 1 se não for nulo 
        if not email:
            raise ValueError('Email vazio')
        
        # 2 - estrutura
        email_lista = email
        email_lista = email_lista.split('@')
        
        # verifica se tem @
        if "@" not in email:
            raise ValueError("email invalido - sem @")

        #verifica se tem nome e dominio
        if len(email_lista) != 2:
            raise ValueError("email invalido - incompleto")

        # verifica se tem ponto
        if '.' not in email_lista[1]:
            raise ValueError("email invalido - incompleto - falta ponto")
        
        # 3 - Caracteres válidos
        #Permitido no local-part (antes do @):
        #letras, números, ., _, -, +
        
        ALLOWED_LOCAL_PART_CHARS = set(
            "abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "0123456789"
            "._-+"
        )

        for letra in email_lista[0]:
            if not letra in ALLOWED_LOCAL_PART_CHARS:
                raise ValueError("email invalido - caracter invalido")
        
        # 4 - Domínio minimamente plausível
        # domínio não pode começar ou terminar com -
        # extensão com pelo menos 2 letras

        # anlise dominio e extenção
        email_tail = email_lista[1].split('.')
        exten = email_tail[-1]
        domin = email_tail[:-1]
    
        # verifica dominio - numeros invalidos
        if not exten.isalpha():
            raise ValueError("Email invalido - dominio caracter invalido")

        # verifica dominio - dominio curto
        if len(exten) < 2:
            raise ValueError('Email invalido - dominio curto')

        for label in domin:
        
            if label[0] == '-' or label[-1] == '-':
                raise ValueError('Emain invalido - caracter invalido')
        
            if not label.replace('-','').isalnum():
                raise ValueError('email invalido - carater invalido ')

        # tratamento email 
        # retira espaços
        email = email.strip()
        print(email)

        # tudo minusculo
        email_person = email.lower()

        return email_person
