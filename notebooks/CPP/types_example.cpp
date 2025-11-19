
// Inclui a biblioteca padrão de entrada/saída
#include <iostream>

// Inclui a biblioteca de string
#include <string>

// Usa o namespace std para evitar escrever std:: o tempo todo
using namespace std;

// Função simples que soma dois inteiros
int add(int a, int b) { 
    return a + b; 
}

int main() {
    // Declara variáveis de diferentes tipos numéricos
    int a = 3;                         // Inteiro simples
    float b = 0.23f;                   // Número de ponto flutuante (precisão simples)
    double c = 0.225678391734;         // Número de ponto flutuante (alta precisão)
    string s = "developer";            // String comum

    // Exibe os valores das variáveis
    cout << "a = " << a << "\n";
    cout << "b = " << b << "\n";
    cout << "c = " << c << "\n";

    // Acessa o primeiro caractere da string
    cout << "s[0] = " << s[0] << "\n";

    // Chama a função add(2,5) e mostra o resultado
    cout << "sum(2,5) = " << add(2,5) << endl;

    // Retorno indicando sucesso
    return 0;
}
