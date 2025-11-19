#include <iostream>   // Permite usar cout, cin e outras funções de entrada/saída
#include <map>        // Fornece o container associativo std::map
#include <string>     // Necessário para trabalhar com std::string

using namespace std;  // Evita escrever std:: antes de cout, map, string etc.

int main() {
    // Declara um map que associa uma string (nome do personagem)
    // a um int (quantidade de episódios)
    map<string,int> episodes;

    // Insere valores no map.
    // A chave é o nome, o valor é a quantidade de episódios.
    episodes["Dolores"] = 30;      // Dolores aparece em 30 episódios
    episodes["Maeve"] = 27;        // Maeve aparece em 27 episódios
    episodes["Theresa"] = 6;       // Theresa aparece em 6 episódios
    episodes["Clementine"] = 11;   // Clementine aparece em 11 episódios

    // Percorre todos os elementos do map utilizando um laço for-each
    // 'auto item' representa um par (pair<string,int>)
    // item.first  → chave (nome)
    // item.second → valor (episódios)
    for (auto item : episodes) {
        cout << item.first           // imprime o nome do personagem
             << " appears in " 
             << item.second          // imprime o número de episódios
             << " episodes\n";
    }

    return 0; // Retorna 0 indicando execução bem-sucedida
}
