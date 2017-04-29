#include <iostream>
#include <sstream>
#include <string>
#include <fstream>

int main(){
	std::ifstream alphafile; 
	std::string s("weights.txt");
	alphafile.open(s.s_char());
	std::string sline;
	std::getline(alphafile,sline);
	std::istringstream iss(sline);
	for (&auto item : iss)
	{
		std::cout<<item<<std::endl;
	}
	return 0;
}