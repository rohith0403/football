from faker import Faker

# Create Faker instances for Brazilian Portuguese and Norwegian locales
fake_brazil = Faker("pt_BR")
fake_norway = Faker("no_NO")

# Generate Brazilian names
print("Brazilian name:", fake_brazil.name_male())

# Generate Norwegian names
print("Norwegian name:", fake_norway.name_male())
