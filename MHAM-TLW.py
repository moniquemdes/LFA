import random

class Transicao:
    def __init__(self, estadoOrigem, variavel, estadoDestino):
        self.estadoOrigem = estadoOrigem
        self.variavel = variavel
        self.estadoDestino = estadoDestino

class AFD:
    def __init__(self, nome, alfabeto, estados, estadoInicial, estadosFinais, transicoes):
        self.nome = nome
        self.alfabeto = alfabeto
        self.estados = estados
        self.estadoInicial = estadoInicial
        self.estadosFinais = estadosFinais
        self.transicoes = transicoes
        self.estadoAtual = estadoInicial

    def ValidarString(self, string):
        estado_atual = self.estadoInicial
        str_length = len(string)

        for i in range(str_length):
            c = string[i]
            transicao_encontrada = False

            for j in range(len(self.transicoes)):
                if self.transicoes[j].estadoOrigem == estado_atual and self.transicoes[j].variavel == c:
                    estado_atual = self.transicoes[j].estadoDestino
                    transicao_encontrada = True
                    break

            if not transicao_encontrada:
                return False

        for i in range(len(self.estados)):
            if estado_atual == self.estadosFinais[i]:
                return True

        return False
    
    def RealizarTransicao(self, variavel):
        for transicao in self.transicoes:
            if(transicao.estadoOrigem == self.estadoAtual):
                if(transicao.variavel == variavel):
                    self.estadoAtual = transicao.estadoDestino
                    return True
    
class Produto:
    def __init__(self, nome, preco, estoqueAtual):
        self.nome = nome
        self.preco = preco
        self.estoqueAtual = estoqueAtual

class Maquina:
    def __init__(self, maquinaVendas, maquinaManutencao, maquinaPagamento):
        self.maquinaVendas = maquinaVendas
        self.maquinaManutencao = maquinaManutencao
        self.maquinaPagamento = maquinaPagamento
        self.bufferProdutos = []
        self.automatosMaquina = [self.maquinaVendas, self.maquinaManutencao, self.maquinaPagamento]
        self.produtos = []
        self.concorrentes = []
        self.sincronizados = []
        self.resultados = []

    def AdicionarBuffer(self, buffer):
        self.bufferProdutos.append(buffer)
        self.automatosMaquina.append(buffer)

    def PopularBuffer(self):
        mod = 1
        for buffer in self.bufferProdutos:
            contItens = random.randint(0, 5)
            self.produtos.append(Produto("Produto " + str(mod), random.randint(1, 9), contItens))
            print("# Populando buffer: " + buffer.nome + " com " + str(contItens) + " itens.")
            self.RealizarTransicao("ini_rep_p0" + str(mod))
            for i in range(contItens):
                self.RealizarTransicao("rep_p0" + str(mod))
            self.RealizarTransicao("fim_rep_p0" + str(mod))
            mod += 1

    def ListarProdutos(self):
        print("\nProdutos na máquina: ")
        for prod in self.produtos:
            print("-> " + prod.nome + " | Preço: R$" + str(prod.preco) + " | Estoque: " + str(prod.estoqueAtual))

    def ObterProduto(self, codigo):
        self.RealizarTransicao("0" + str(codigo) + "_sel")
        if(self.bufferProdutos[codigo - 1].estadoAtual == self.bufferProdutos[codigo - 1].estadoInicial):
            self.RealizarTransicao("n_tem_p0" + str(codigo))
            return False
        else:
            self.RealizarTransicao("tem_p0" + str(codigo))
            return True

    def RealizarTransicao(self, variavel):
        cont = 0
        for afd in self.automatosMaquina:
            if(afd.RealizarTransicao(variavel)):
                self.resultados.append("O autômato [" + afd.nome + "] realizou a transição [" + variavel + "]. Estado atual do autômato é [" + afd.estadoAtual + "]")
                cont += 1
        if(cont > 1):
            if(variavel not in self.sincronizados):
                #print("# Adicionando em sincronizados " + variavel)
                self.sincronizados.append(variavel)
        else:
            if(variavel not in self.concorrentes):
                #print("# Adicionando em concorrentes " + variavel)
                self.concorrentes.append(variavel)

    def ListarSincronizados(self):
        print("\n--------------------------")
        print("# Transições Sincronizadas")
        for sinc in self.sincronizados:
            print("  #-> " + sinc)

    def ListarConcorrentes(self):
        print("\n--------------------------")
        print("# Transições Concorrentes")
        for conc in self.concorrentes:
            print("  #-> " + conc)

    def ListarResultados(self):
        print("\n--------------------------")
        print("# Resumo do funcionamento: ")
        for result in self.resultados:
            print("  #-> " + result)

    def RetornarPrecoProduto(self, codigo):
        return self.produtos[codigo - 1].preco

    def ChecarPagamento(self, codigo, carteira):
        self.RealizarTransicao("ini_pg_p0" + str(codigo))
        opcaoPagamento = int(input("Como deseja pagar? 1. Cartão ou 2. Dinheiro: "))
        if(opcaoPagamento == 1):
            self.RealizarTransicao("pg_cartao_p0" + str(codigo))
            if(self.produtos[codigo - 1].preco <= carteira):
                print("Você passou o cartão e agora tem " + str(carteira - self.produtos[codigo - 1].preco) + " na sua conta.")
                self.RealizarTransicao("pg_ok_p0" + str(codigo))
                self.RealizarTransicao("conf_pg_p0" + str(codigo))
                return True                
            else:
                self.RealizarTransicao("pg_nok_p0" + str(codigo))
                self.RealizarTransicao("n_conf_pg_p0" + str(codigo))
                return False                 
        else:
            self.RealizarTransicao("pg_cash_p0" + str(codigo))
            if(self.produtos[codigo].preco <= carteira):
                self.RealizarTransicao("pg_ok_p0" + str(codigo))
                if(self.produtos[codigo].preco == carteira):
                    print("Você deu todo seu dinheiro a máquina, e esse era o preço do produto. Você ficou sem dinheiro.")
                    self.RealizarTransicao("n_troco_p0" + str(codigo))
                    self.RealizarTransicao("conf_pg_p0" + str(codigo))
                    return True                 
                else:
                    print("Você deu todo seu dinheiro a máquina. Você recebeu " + str(carteira - self.produtos[codigo - 1].preco) + " de troco.")
                    self.RealizarTransicao("troco_p0" + str(codigo))
                    self.RealizarTransicao("conf_pg_p0" + str(codigo))
                    return True                 
            else:
                self.RealizarTransicao("pg_nok_p0" + str(codigo))         
                self.RealizarTransicao("n_conf_pg_p0" + str(codigo))
                return False


def main():
    maquinaVendas = AFD(
        "Máquina de vendas", # Nome do autômato
        {"ini_man", "fim_man", "01_sel", "02_sel", "03_sel", "04_sel", "05_sel", "n_tem_p01", "n_tem_p02", "n_tem_p03", "n_tem_p04", "n_tem_p05", "n_conf_pg_p01", "n_conf_pg_p02", "n_conf_pg_p03", "n_conf_pg_p04", "n_conf_pg_p05", "tem_p01", "tem_p02", "tem_p03", "tem_p04", "tem_p05", "ini_pg_p01", "ini_pg_p02", "ini_pg_p03", "ini_pg_p04", "ini_pg_p05", "conf_pg_p01", "conf_pg_p02", "conf_pg_p03", "conf_pg_p04", "conf_pg_p05", "ini_ent_p01", "ini_ent_p02", "ini_ent_p03", "ini_ent_p04", "ini_ent_p05", "ven_p01", "ven_p02", "ven_p03", "ven_p04", "ven_p05", "fim_ent_p01", "fim_ent_p02", "fim_ent_p03", "fim_ent_p04", "fim_ent_p05"}, # Alfabeto
        {"0_sel", "01_se", "02_se", "03_se", "04_se", "05_se", "01_te", "02_te", "03_te", "04_te", "05_te", "01_ip", "02_ip", "03_ip", "04_ip", "05_ip", "01_cp", "02_cp", "03_cp", "04_cp", "05_cp", "01_ie", "02_ie", "03_ie", "04_ie", "05_ie", "01_fe", "02_fe", "03_fe", "04_fe", "05_fe", "man"}, # Estados
        "0_sel", # Estado inicial
        {"0_sel", "01_se", "02_se", "03_se", "04_se", "05_se", "01_te", "02_te", "03_te", "04_te", "05_te", "01_ip", "02_ip", "03_ip", "04_ip", "05_ip", "01_cp", "02_cp", "03_cp", "04_cp", "05_cp", "01_ie", "02_ie", "03_ie", "04_ie", "05_ie", "01_fe", "02_fe", "03_fe", "04_fe", "05_fe", "man"}, # Estados finais
        {
            Transicao("01_se", "tem_p01", "01_te"),
            Transicao("02_se", "tem_p02", "02_te"),
            Transicao("03_se", "tem_p03", "03_te"),
            Transicao("04_se", "tem_p04", "04_te"),
            Transicao("05_se", "tem_p05", "05_te"),
            Transicao("01_se", "n_tem_p01", "0_sel"),
            Transicao("02_se", "n_tem_p02", "0_sel"),
            Transicao("03_se", "n_tem_p03", "0_sel"),
            Transicao("04_se", "n_tem_p04", "0_sel"),
            Transicao("05_se", "n_tem_p05", "0_sel"),
            Transicao("01_te", "ini_pg_p01", "01_ip"),
            Transicao("02_te", "ini_pg_p02", "02_ip"),
            Transicao("03_te", "ini_pg_p03", "03_ip"),
            Transicao("04_te", "ini_pg_p04", "04_ip"),
            Transicao("05_te", "ini_pg_p05", "05_ip"),
            Transicao("01_ip", "n_conf_pg_p01", "0_sel"),
            Transicao("02_ip", "n_conf_pg_p02", "0_sel"),
            Transicao("03_ip", "n_conf_pg_p03", "0_sel"),
            Transicao("04_ip", "n_conf_pg_p04", "0_sel"),
            Transicao("05_ip", "n_conf_pg_p05", "0_sel"),
            Transicao("01_ip", "conf_pg_p01", "01_cp"),
            Transicao("02_ip", "conf_pg_p02", "02_cp"),
            Transicao("03_ip", "conf_pg_p03", "03_cp"),
            Transicao("04_ip", "conf_pg_p04", "04_cp"),
            Transicao("05_ip", "conf_pg_p05", "05_cp"),
            Transicao("01_cp", "ini_ent_p01", "01_ie"),
            Transicao("02_cp", "ini_ent_p02", "02_ie"),
            Transicao("03_cp", "ini_ent_p03", "03_ie"),
            Transicao("04_cp", "ini_ent_p04", "04_ie"),
            Transicao("05_cp", "ini_ent_p05", "05_ie"),
            Transicao("01_ie", "ven_p01", "01_fe"),
            Transicao("02_ie", "ven_p02", "02_fe"),
            Transicao("03_ie", "ven_p03", "03_fe"),
            Transicao("04_ie", "ven_p04", "04_fe"),
            Transicao("05_ie", "ven_p05", "05_fe"),
            Transicao("01_fe", "fim_ent_p01", "0_sel"),
            Transicao("02_fe", "fim_ent_p02", "0_sel"),
            Transicao("03_fe", "fim_ent_p03", "0_sel"),
            Transicao("04_fe", "fim_ent_p04", "0_sel"),
            Transicao("05_fe", "fim_ent_p05", "0_sel"),
            Transicao("0_sel", "ini_man", "man"),
            Transicao("0_sel", "01_sel", "01_se"),
            Transicao("0_sel", "02_sel", "02_se"),
            Transicao("0_sel", "03_sel", "03_se"),
            Transicao("0_sel", "04_sel", "04_se"),
            Transicao("0_sel", "05_sel", "05_se"),
            Transicao("man", "fim_man", "0_sel")
        } # Transições
    )

    maquinaManutencao = AFD(
        "Máquina de Manutenção",
        {"ini_man", "fim_man", "fim_rep_p01", "ini_rep_p01", "rep_p01", "fim_rep_p02", "ini_rep_p02", "rep_p02", "fim_rep_p03", "ini_rep_p03", "rep_p03", "fim_rep_p04", "ini_rep_p04", "rep_p04", "fim_rep_p05", "ini_rep_p05", "rep_p05"}, # Alfabeto
        {"0_mt", "1_mt", "01_rp", "02_rp", "03_rp", "04_rp", "05_rp"}, # Estados
        "0_mt", # Estado Inicial
        {"0_mt", "1_mt", "01_rp", "02_rp", "03_rp", "04_rp", "05_rp"}, # Estados Finais
        {
            Transicao("0_mt", "ini_man", "1_mt"), 
            Transicao("1_mt", "fim_man", "0_mt"),
            Transicao("1_mt", "ini_rep_p01", "01_rp"), 
            Transicao("01_rp", "rep_p01", "01_rp"),
            Transicao("01_rp", "fim_rep_p01", "1_mt"), 
            Transicao("1_mt", "ini_rep_p02", "02_rp"),
            Transicao("02_rp", "rep_p02", "02_rp"), 
            Transicao("02_rp", "fim_rep_p02", "1_mt"),
            Transicao("1_mt", "ini_rep_p03", "03_rp"), 
            Transicao("03_rp", "rep_p03", "03_rp"),
            Transicao("03_rp", "fim_rep_p03", "1_mt"), 
            Transicao("1_mt", "ini_rep_p04", "04_rp"),
            Transicao("04_rp", "rep_p04", "04_rp"), 
            Transicao("04_rp", "fim_rep_p04", "1_mt"),
            Transicao("1_mt", "ini_rep_p05", "05_rp"),
            Transicao("05_rp", "rep_p05", "05_rp"), 
            Transicao("05_rp", "fim_rep_p05", "1_mt")
        } # Transições
    )

    maquinaPagamento = AFD(
        "Máquina de Pagamento",
        {"conf_pg01", "conf_pg02", "conf_pg03", "conf_pg04", "conf_pg05", "ini_pg_p01", "ini_pg_p02", "ini_pg_p03", "ini_pg_p04", "ini_pg_p05", "pg_cash_p01", "pg_cash_p02", "pg_cash_p03", "pg_cash_p04", "pg_cash_p05", "pg_cartao_p01", "pg_cartao_p02", "pg_cartao_p03", "pg_cartao_p04", "pg_cartao_p05", "pg_ok_p01", "pg_ok_p02", "pg_ok_p03", "pg_ok_p04", "pg_ok_p05", "pg_nok_p01", "pg_nok_p02", "pg_nok_p03", "pg_nok_p04", "pg_nok_p05", "troco_p01", "troco_p02", "troco_p03", "troco_p04", "troco_p05", "n_troco_p01", "n_troco_p02", "n_troco_p03", "n_troco_p04", "n_troco_p05"},
        {"0_vd", "1_vd1", "2_vd1", "3_vd1", "4_vd1", "5_vd1", "6_vd1", "7_vd1", "1_vd2", "2_vd2", "3_vd2", "4_vd2", "5_vd2", "6_vd2", "7_vd2", "1_vd3", "2_vd3", "3_vd3", "4_vd3", "5_vd3", "6_vd3", "7_vd3", "1_vd4", "2_vd4", "3_vd4", "4_vd4", "5_vd4", "6_vd4", "7_vd4", "1_vd5", "2_vd5", "3_vd5", "4_vd5", "5_vd5", "6_vd5", "7_vd5"},
        "0_vd",
        {"0_vd", "1_vd1", "2_vd1", "3_vd1", "4_vd1", "5_vd1", "6_vd1", "7_vd1", "1_vd2", "2_vd2", "3_vd2", "4_vd2", "5_vd2", "6_vd2", "7_vd2", "1_vd3", "2_vd3", "3_vd3", "4_vd3", "5_vd3", "6_vd3", "7_vd3", "1_vd4", "2_vd4", "3_vd4", "4_vd4", "5_vd4", "6_vd4", "7_vd4", "1_vd5", "2_vd5", "3_vd5", "4_vd5", "5_vd5", "6_vd5", "7_vd5"},
        {
            Transicao("0_vd", "ini_pg_p01", "1_vd1"),
            Transicao("1_vd1", "pg_cash_p01", "2_vd1"),
            Transicao("1_vd1", "pg_cartao_p01", "3_vd1"),
            Transicao("2_vd1", "pg_ok_p01", "4_vd1"),
            Transicao("2_vd1", "pg_nok_p01", "5_vd1"),
            Transicao("3_vd1", "pg_nok_p01", "5_vd1"),
            Transicao("3_vd1", "pg_ok_p01", "7_vd1"),
            Transicao("4_vd1", "troco_p01", "6_vd1"),
            Transicao("4_vd1", "n_troco_p01", "6_vd1"),
            Transicao("5_vd1", "n_cong_pg_01", "0_vd"),
            Transicao("6_vd1", "conf_pg_p01", "0_vd"),
            Transicao("7_vd1", "conf_pg_p01", "0_vd"),
            Transicao("0_vd", "ini_pg_p02", "1_vd2"),
            Transicao("1_vd2", "pg_cash_p02", "2_vd2"),
            Transicao("1_vd2", "pg_cartao_p02", "3_vd2"),
            Transicao("2_vd2", "pg_ok_p02", "4_vd2"),
            Transicao("2_vd2", "pg_nok_p02", "5_vd2"),
            Transicao("3_vd2", "pg_nok_p02", "5_vd2"),
            Transicao("3_vd2", "pg_ok_p02", "7_vd2"),
            Transicao("4_vd2", "troco_p02", "6_vd2"),
            Transicao("4_vd2", "n_troco_p02", "6_vd2"),
            Transicao("5_vd2", "n_cong_pg_02", "0_vd"),
            Transicao("6_vd2", "conf_pg_p02", "0_vd"),
            Transicao("7_vd2", "conf_pg_p02", "0_vd"),
            Transicao("0_vd", "ini_pg_p03", "1_vd3"),
            Transicao("1_vd3", "pg_cash_p03", "2_vd3"),
            Transicao("1_vd3", "pg_cartao_p03", "3_vd3"),
            Transicao("2_vd3", "pg_ok_p03", "4_vd3"),
            Transicao("2_vd3", "pg_nok_p03", "5_vd3"),
            Transicao("3_vd3", "pg_nok_p03", "5_vd3"),
            Transicao("3_vd3", "pg_ok_p03", "7_vd3"),
            Transicao("4_vd3", "troco_p03", "6_vd3"),
            Transicao("4_vd3", "n_troco_p03", "6_vd3"),
            Transicao("5_vd3", "n_cong_pg_03", "0_vd"),
            Transicao("6_vd3", "conf_pg_p03", "0_vd"),
            Transicao("7_vd3", "conf_pg_p03", "0_vd"),
            Transicao("0_vd", "ini_pg_p04", "1_vd4"),
            Transicao("1_vd4", "pg_cash_p04", "2_vd4"),
            Transicao("1_vd4", "pg_cartao_p04", "3_vd4"),
            Transicao("2_vd4", "pg_ok_p04", "4_vd4"),
            Transicao("2_vd4", "pg_nok_p04", "5_vd4"),
            Transicao("3_vd4", "pg_nok_p04", "5_vd4"),
            Transicao("3_vd4", "pg_ok_p04", "7_vd4"),
            Transicao("4_vd4", "troco_p04", "6_vd4"),
            Transicao("4_vd4", "n_troco_p04", "6_vd4"),
            Transicao("5_vd4", "n_cong_pg_04", "0_vd"),
            Transicao("6_vd4", "conf_pg_p04", "0_vd"),
            Transicao("7_vd4", "conf_pg_p04", "0_vd"),
            Transicao("0_vd", "ini_pg_p05", "1_vd5"),
            Transicao("1_vd5", "pg_cash_p05", "2_vd5"),
            Transicao("1_vd5", "pg_cartao_p05", "3_vd5"),
            Transicao("2_vd5", "pg_ok_p05", "4_vd5"),
            Transicao("2_vd5", "pg_nok_p05", "5_vd5"),
            Transicao("3_vd5", "pg_nok_p05", "5_vd5"),
            Transicao("3_vd5", "pg_ok_p05", "7_vd5"),
            Transicao("4_vd5", "troco_p05", "6_vd5"),
            Transicao("4_vd5", "n_troco_p05", "6_vd5"),
            Transicao("5_vd5", "n_cong_pg_05", "0_vd"),
            Transicao("6_vd5", "conf_pg_p05", "0_vd"),
            Transicao("7_vd5", "conf_pg_p05", "0_vd")
        }
    )

    bufferProd1 = AFD(
        "Buffer Produto 1",
        {"rep_p01", "ven_p01", "n_tem_p01"}, # Alfabeto
        {"0_p1", "1_p1", "2_p1", "3_p1", "4_p1", "5_p1"}, # Estados
        "0_p1", # Estado Inicial
        {"0_p1", "1_p1", "2_p1", "3_p1", "4_p1", "5_p1"}, # Estados Finais
        {
            Transicao("0_p1", "rep_p01", "1_p1"), 
            Transicao("1_p1", "rep_p01", "2_p1"),
            Transicao("2_p1", "rep_p01", "3_p1"), 
            Transicao("3_p1", "rep_p01", "4_p1"),
            Transicao("4_p1", "rep_p01", "5_p1"), 
            Transicao("5_p1", "ven_p01", "4_p1"),
            Transicao("4_p1", "ven_p01", "3_p1"), 
            Transicao("3_p1", "ven_p01", "2_p1"),
            Transicao("2_p1", "ven_p01", "1_p1"), 
            Transicao("1_p1", "ven_p01", "0_p1"),
            Transicao("0_p1", "n_tem_p01", "0_p1"), 
            Transicao("1_p1", "tem_p01", "1_p1"), 
            Transicao("2_p1", "tem_p01", "2_p1"), 
            Transicao("3_p1", "tem_p01", "3_p1"),
            Transicao("4_p1", "tem_p01", "4_p1"), 
            Transicao("5_p1", "tem_p01", "5_p1")
         } # Transições
    )

    bufferProd2 = AFD(
        "Buffer Produto 2",
        {"rep_p02", "ven_p02", "n_tem_p02"}, # Alfabeto
        {"0_p2", "1_p2", "2_p2", "3_p2", "4_p2", "5_p2"}, # Estados
        "0_p2", # Estado Inicial
        {"0_p2", "1_p2", "2_p2", "3_p2", "4_p2", "5_p2"}, # Estados Finais
        {
            Transicao("0_p2", "rep_p02", "1_p2"), 
            Transicao("1_p2", "rep_p02", "2_p2"),
            Transicao("2_p2", "rep_p02", "3_p2"), 
            Transicao("3_p2", "rep_p02", "4_p2"),
            Transicao("4_p2", "rep_p02", "5_p2"), 
            Transicao("5_p2", "ven_p02", "4_p2"),
            Transicao("4_p2", "ven_p02", "3_p2"), 
            Transicao("3_p2", "ven_p02", "2_p2"),
            Transicao("2_p2", "ven_p02", "1_p2"), 
            Transicao("1_p2", "ven_p02", "0_p2"),
            Transicao("0_p2", "n_tem_p02", "0_p2"), 
            Transicao("1_p2", "tem_p02", "1_p2"), 
            Transicao("2_p2", "tem_p02", "2_p2"), 
            Transicao("3_p2", "tem_p02", "3_p2"),
            Transicao("4_p2", "tem_p02", "4_p2"), 
            Transicao("5_p2", "tem_p02", "5_p2")
         } # Transições
    )

    bufferProd3 = AFD(
        "Buffer Produto 3",
        {"rep_p03", "ven_p03", "n_tem_p03"}, # Alfabeto
        {"0_p3", "1_p3", "2_p3", "3_p3", "4_p3", "5_p3"}, # Estados
        "0_p3", # Estado Inicial
        {"0_p3", "1_p3", "2_p3", "3_p3", "4_p3", "5_p3"}, # Estados Finais
        {
            Transicao("0_p3", "rep_p03", "1_p3"), 
            Transicao("1_p3", "rep_p03", "2_p3"),
            Transicao("2_p3", "rep_p03", "3_p3"), 
            Transicao("3_p3", "rep_p03", "4_p3"),
            Transicao("4_p3", "rep_p03", "5_p3"), 
            Transicao("5_p3", "ven_p03", "4_p3"),
            Transicao("4_p3", "ven_p03", "3_p3"), 
            Transicao("3_p3", "ven_p03", "2_p3"),
            Transicao("2_p3", "ven_p03", "1_p3"), 
            Transicao("1_p3", "ven_p03", "0_p3"),
            Transicao("0_p3", "n_tem_p03", "0_p3"), 
            Transicao("1_p3", "tem_p03", "1_p3"), 
            Transicao("2_p3", "tem_p03", "2_p3"), 
            Transicao("3_p3", "tem_p03", "3_p3"),
            Transicao("4_p3", "tem_p03", "4_p3"), 
            Transicao("5_p3", "tem_p03", "5_p3")
        } # Transições
    )

    bufferProd4 = AFD(
        "Buffer Produto 4",
        {"rep_p04", "ven_p04", "n_tem_p04"}, # Alfabeto
        {"0_p4", "1_p4", "2_p4", "3_p4", "4_p4", "5_p4"}, # Estados
        "0_p4", # Estado Inicial
        {"0_p4", "1_p4", "2_p4", "3_p4", "4_p4", "5_p4"}, # Estados Finais
        {
            Transicao("0_p4", "rep_p04", "1_p4"), 
            Transicao("1_p4", "rep_p04", "2_p4"),
            Transicao("2_p4", "rep_p04", "3_p4"), 
            Transicao("3_p4", "rep_p04", "4_p4"),
            Transicao("4_p4", "rep_p04", "5_p4"), 
            Transicao("5_p4", "ven_p04", "4_p4"),
            Transicao("4_p4", "ven_p04", "3_p4"), 
            Transicao("3_p4", "ven_p04", "2_p4"),
            Transicao("2_p4", "ven_p04", "1_p4"), 
            Transicao("1_p4", "ven_p04", "0_p4"),
            Transicao("0_p4", "n_tem_p04", "0_p4"), 
            Transicao("1_p4", "tem_p04", "1_p4"), 
            Transicao("2_p4", "tem_p04", "2_p4"), 
            Transicao("3_p4", "tem_p04", "3_p4"),
            Transicao("4_p4", "tem_p04", "4_p4"), 
            Transicao("5_p4", "tem_p04", "5_p4")
         } # Transições
    )

    bufferProd5 = AFD(
        "Buffer Produto 5",
        {"rep_p05", "ven_p05", "n_tem_p05"}, # Alfabeto
        {"0_p5", "1_p5", "2_p5", "3_p5", "4_p5", "5_p5"}, # Estados
        "0_p5", # Estado Inicial
        {"0_p5", "1_p5", "2_p5", "3_p5", "4_p5", "5_p5"}, # Estados Finais
        {
            Transicao("0_p5", "rep_p05", "1_p5"), 
            Transicao("1_p5", "rep_p05", "2_p5"),
            Transicao("2_p5", "rep_p05", "3_p5"), 
            Transicao("3_p5", "rep_p05", "4_p5"),
            Transicao("4_p5", "rep_p05", "5_p5"), 
            Transicao("5_p5", "ven_p05", "4_p5"),
            Transicao("4_p5", "ven_p05", "3_p5"), 
            Transicao("3_p5", "ven_p05", "2_p5"),
            Transicao("2_p5", "ven_p05", "1_p5"), 
            Transicao("1_p5", "ven_p05", "0_p5"),
            Transicao("0_p5", "n_tem_p05", "0_p5"), 
            Transicao("1_p5", "tem_p05", "1_p5"), 
            Transicao("2_p5", "tem_p05", "2_p5"), 
            Transicao("3_p5", "tem_p05", "3_p5"),
            Transicao("4_p5", "tem_p05", "4_p5"), 
            Transicao("5_p5", "tem_p05", "5_p5")
        } # Transições
    )

    maquina = Maquina(maquinaVendas, maquinaManutencao, maquinaPagamento)

    maquina.AdicionarBuffer(bufferProd1)
    maquina.AdicionarBuffer(bufferProd2)
    maquina.AdicionarBuffer(bufferProd3)
    maquina.AdicionarBuffer(bufferProd4)
    maquina.AdicionarBuffer(bufferProd5)
    
    maquina.RealizarTransicao("ini_man")
    maquina.PopularBuffer()
    maquina.RealizarTransicao("fim_man")

    carteira = random.randint(20, 200)


    while True:
        maquina.ListarProdutos()
        print("\nVocê tem R$" + str(carteira) + " em seu cartão e/ou carteira.")
        opcao = int(input("\nDigite o código do produto (1 - 5) ou digite 0 para sair: "))
        
        if(opcao == 0):
            print("Encerrando...")
            break

        if(opcao > 0 and opcao < 6):
            if(maquina.ObterProduto(opcao)):
                if(maquina.ChecarPagamento(opcao, carteira)):
                    carteira -= maquina.RetornarPrecoProduto(opcao)
                    maquina.RealizarTransicao("ini_ent_p0" + str(opcao))
                    maquina.RealizarTransicao("ven_p0" + str(opcao))
                    maquina.RealizarTransicao("fim_ent_p0" + str(opcao))
                    maquina.produtos[opcao - 1].estoqueAtual -= 1
                    print("Produto entregue!")
                else:
                    print("Erro no pagamento!")
            else:
                print("O produto que você escolheu não tem em estoque. Escolha outro por favor!")
        else:
            print("Código inválido. Tente de novo.")

    maquina.ListarConcorrentes()
    maquina.ListarSincronizados()

    maquina.ListarResultados()

if __name__ == "__main__":
    main()
