#include <iostream>
#include <string.h>
#include <fstream>
#include <math.h>
#include <vector>
#include <limits.h>

class point
{
	// point : class for defining a location
public:
	int x;
	int y;
	point(int X, int Y):x(X),y(Y){};
	~point(){};
	int getMdistance(point P) {
		// returns the manhataan distance between two points
	return fabs(x - P.x) + fabs(y - P.y);
} 

};
class rewardmap
{
private:
	std::vector<double> alpha ;	// weights of features, to be read from a file at location 'address'
	std::vector<point> obs;		// location of obstacles
	std::vector<point> coin;	// location of coins
	int grid_size;				// size of grid
public:
	rewardmap(std::string& address, int& Grid , std::vector<point>& Obs,std::vector<point>& Coin);
	~rewardmap(){};
	double getReward(point player);

};