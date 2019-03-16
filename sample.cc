#include <list>
#include <unordered_map>
#include <string>


int main() {
    std::list<int> a;
    std::unordered_map<std::string, int> b;
    a = b;
}
