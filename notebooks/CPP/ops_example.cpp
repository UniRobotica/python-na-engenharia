
// Biblioteca padrão de entrada e saída (cout, endl)
#include <iostream>

// Facilita o uso de cout, endl, etc.
using namespace std;

int main() {

    // Declara duas variáveis para operações aritméticas
    int a = 4, b = 3;

    // Soma: 4 + 3 = 7
    cout << (a + b) << endl;

    // Subtração: 4 - 3 = 1
    cout << (a - b) << endl;

    // Multiplicação: 4 * 3 = 12
    cout << (a * b) << endl;

    // Divisão inteira: 4 / 3 = 1  (parte inteira apenas)
    cout << (a / b) << endl;

    // Módulo (resto da divisão): 4 % 3 = 1
    cout << (a % b) << endl;

    // Demonstração de operadores de atribuição abreviados
    int x = 5;

    // x += 2  →  x = x + 2  →  x passa a valer 7
    cout << (x += 2) << endl;

    // x *= 2  →  x = x * 2  →  x passa a valer 14
    cout << (x *= 2) << endl;

    // Comparações lógicas (true = 1, false = 0)
    int y = 9, z = 8;

    // y == z  →  9 == 8  → falso → 0
    cout << (y == z) << endl;

    // y > z  →  9 > 8  → verdadeiro → 1
    cout << (y > z) << endl;

    // y < z  →  9 < 8  → falso → 0
    cout << (y < z) << endl;

    // Fim do programa
    return 0;
}

