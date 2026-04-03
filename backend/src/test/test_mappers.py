from src.infra.db.entities.entity_person import PersonEntity
from src.infra.db.entities.entity_customer import CustomerEntity
from src.domain.models.model_person import PersonModel
from src.domain.models.model_customer import CustomerModel
from src.infra.db.mappers.mapper import DataMapper

def test_person_mapper():
    print("🧪 Iniciando Teste de Mapeamento...")

    # 1. DADOS DE ENTRADA (Simulando o que vem do Front-end)
    dados_frontend = {
        "name": "Luiz Santanna",
        "cpf": "12345678901",
        "cnpj": "12345678000199",
        "phone": "21988887777",
        "email": "sant@email.com",
        "password": "senha_ultra_secreta"
    }

    # Criamos o Model (Pydantic)
    model_entrada = PersonModel(**dados_frontend)
    print("✅ Model Pydantic criado.")

    # ---------------------------------------------------------
    # TESTE 1: MODEL -> ENTITY (Indo para o Banco)
    # ---------------------------------------------------------
    entidade = DataMapper.model_to_entity(model_entrada, PersonEntity)

    print("\n--- Verificando Conversão para Entity ---")
    assert isinstance(entidade, PersonEntity), "Erro: Não converteu para PersonEntity"
    assert entidade.name == "Luiz Santanna"
    assert entidade.email == "sant@email.com"
    print(f"✅ Nome na Entity: {entidade.name}")
    print(f"✅ Email na Entity: {entidade.email}")

    # ---------------------------------------------------------
    # TESTE 2: ENTITY -> MODEL (Voltando para o Objeto de Dados)
    # ---------------------------------------------------------
    # Simulamos que o banco de dados gerou um ID automático
    entidade.id = 50 

    model_saida = DataMapper.entity_to_model(entidade, PersonModel)

    print("\n--- Verificando Conversão de Volta para Model ---")
    assert isinstance(model_saida, PersonModel), "Erro: Não converteu para PersonModel"
    assert model_saida.id == 50
    assert model_saida.name == "Luiz Santanna"
    print(f"✅ ID no Model de saída: {model_saida.id}")
    print(f"✅ Nome no Model de saída: {model_saida.name}")

    print("\n[SUCESSO] O DataMapper está integrando Model e Entity corretamente! 🎉")

if __name__ == "__main__":
    test_person_mapper()