from src.infra.db.repositores.repository_customer import CustomerRepository
from src.infra.db.repositores.repository_person import PersonRepository
from src.infra.db.entities.entity_customer import CustomerEntity
from src.domain.models.model_customer import CustomerModel
from src.infra.db.mappers.mapper import DataMapper



customer_test = CustomerModel(
    name="teste repositorio LTDA",
    cnpj="99888777000166",
    phone="2133334444",
    email="contato@empresa.com",
    id_person = 1
)

def test_crate_customer():
    repo = CustomerRepository(mapper= DataMapper)
    result = repo.create_customer(model_customer= customer_test)
    print(f"resposta: {result}")

def test_read_customer():
    repo = CustomerRepository(mapper= DataMapper)
    result = repo.read_customer(id_person= 1)
    print(f"resposta: {result}")