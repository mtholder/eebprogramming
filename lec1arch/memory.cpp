#include <iostream>
using namespace std;
int main(int argc, char * argv[]) {
	for (int i = 0; i <= 126; ++i) {
		char c = (char) i;
		cout << i << "\t\"" << c << "\"\n";
	}
	return 0;
}
