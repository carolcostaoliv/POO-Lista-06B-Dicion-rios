from datetime import datetime
import json

class Contato:
    def __init__(self, i, n, e, f, b):
        self.__id = i
        self.__nome = n
        self.__email = e
        self.__fone = f
        self.__nasc = b
        self.set_nasc(self.__nasc)

    def set_nasc(self, b):
        if b > datetime.today(): 
            raise ValueError("A data de nascimento é inválida")
        self.__nasc = b

    def get_nasc(self):
        return self.__nasc

    def set_nome(self, nome2):
        self.__nome = nome2

    def get_nome(self):
        return self.__nome

    def get_id(self):
        return self.__id 

    def set_email(self, email2):
        self.__email = email2

    def get_email(self):
        return self.__email

    def set_fone(self, fone2):
        self.__fone = fone2

    def get_fone(self):
        return self.__fone

    def __str__(self):
        return f"{self.__id} - {self.__nome} - {self.__email} - {self.__fone} - {self.__nasc.strftime('%d/%m/%Y')}"

    def para_dict(self):
        return {
            "id": self.__id,
            "nome": self.__nome,
            "email": self.__email,
            "fone": self.__fone,
            "nasc": self.__nasc.strftime("%d/%m/%Y")  
        }

    @staticmethod
    def de_dict(d):
        nasc = datetime.strptime(d["nasc"], "%d/%m/%Y")
        return Contato(d["id"], d["nome"], d["email"], d["fone"], nasc)

class ContatoUI:
    __contatos = []
    __arquivo = "contatos.json"

    @classmethod
    def main(cls):
        cls.carregar()
        op = 0
        while op != 7:
            op = cls.menu()
            if op == 1: cls.inserir()
            if op == 2: cls.listar()
            if op == 3: cls.atualizar()
            if op == 4: cls.excluir()
            if op == 5: cls.pesquisar()
            if op == 6: cls.aniversariantes()
        cls.salvar()

    @classmethod
    def menu(cls):
        print("1-Inserir, 2-Listar, 3-Atualizar, 4-Excluir, 5-Pesquisar, 6-Aniversariantes, 7-Fim")
        return int(input("Informe uma opção: "))

    @classmethod
    def inserir(cls):
        nome = input("Informe o nome: ")
        email = input("Informe o e-mail: ")
        fone = input("Informe o fone: ")
        nasc = datetime.strptime(input("Informe a data de nascimento: "), "%d/%m/%Y")
        for c in cls.__contatos:
            if c.get_email() == email:
                print("Email já cadastrado. Digite novamente")
                return
        id = 1
        if cls.__contatos:
            id = max(c.get_id() for c in cls.__contatos) + 1
        c = Contato(id, nome, email, fone, nasc)
        cls.__contatos.append(c)
        print("Contato inserido com sucesso!")

    @classmethod
    def listar(cls):
        if not cls.__contatos:
            print("Nenhum contato cadastrado")
        else:
            for c in cls.__contatos:
                print(c)

    @classmethod
    def listar_id(cls, id):
        for c in cls.__contatos:
            if c.get_id() == id: return c
        return None    

    @classmethod
    def atualizar(cls):
        cls.listar()
        id = int(input("Informe o id do contato a ser atualizado: "))
        c = cls.listar_id(id)
        if c == None: 
            print("Esse contato não existe")
        else:
            nome2 = input("Informe o novo nome: ")
            email2 = input("Informe o novo email: ")
            fone2 = input("Informe o novo fone: ")
            c.set_nome(nome2)
            c.set_email(email2)
            c.set_fone(fone2)
            print("Contato atualizado")

    @classmethod
    def excluir(cls):
        cls.listar()
        id = int(input("Informe o id do contato a ser excluído: "))
        c = cls.listar_id(id)
        if c == None: 
            print("Esse contato não existe")
        else: 
            cls.__contatos.remove(c)
            print("Contato excluído")

    @classmethod
    def pesquisar(cls):
        nome = input("Informe o nome do contato: ")
        achou = False
        for c in cls.__contatos:
            if c.get_nome().lower().startswith(nome.lower()):
                print(c)
                achou = True
        if not achou:
            print("Nenhum contato encontrado com esse nome.")

    @classmethod
    def aniversariantes(cls):
        mes = int(input("Informe o mês para ver os aniversariantes: "))
        achou = False
        for c in cls.__contatos:
            if c.get_nasc().month == mes:
                print(c)
                achou = True
        if not achou:
            print("Não há nenhum contato que faz aniversário nesse mês")

    @classmethod
    def salvar(cls):
        dados = [c.para_dict() for c in cls.__contatos]
        with open(cls.__arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4)
        print("Contatos salvos com sucesso!")

    @classmethod
    def carregar(cls):
        try:
            with open(cls.__arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
                cls.__contatos = [Contato.de_dict(d) for d in dados]
        except FileNotFoundError:
            cls.__contatos = []

ContatoUI.main()