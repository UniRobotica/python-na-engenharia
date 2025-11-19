
#include <iostream>
#include <list>
using namespace std;

int main(){
    list<int> numbers = {1, 10, 100, 1000};
    numbers.push_front(0);
    numbers.push_back(3000);

    for (int val : numbers) {
        cout << val << " ";
    }
    cout << endl;
    return 0;
}
