class ElementoEstrutural:
    def __init__(self, identificacao, material):
        self.identificacao = identificacao
        self.material = material

    def descrever(self):
        return f"{self.identificacao} - Material: {self.material}"


class Viga(ElementoEstrutural):
    def __init__(self, identificacao, material,
                 comprimento, largura, altura):
        super().__init__(identificacao, material)
        self.comprimento = comprimento
        self.largura = largura
        self.altura = altura

    def calcular_volume(self):
        return self.comprimento * self.largura * self.altura


class Pilar(ElementoEstrutural):
    def __init__(self, identificacao, material,
                 largura, profundidade, altura):
        super().__init__(identificacao, material)
        self.largura = largura
        self.profundidade = profundidade
        self.altura = altura

    def calcular_volume(self):
        return self.largura * self.profundidade * self.altura