#include "reward.hpp"

int main()
{
	std::vector<point> obs,coin;
	obs.push_back(point(2,3));
	obs.push_back(point(1,2));
	coin.push_back(point(5,5));
	point player(3,5);
	std::string addr("let party play");
	int grid_size = 7;
	rewardmap rmap(addr,grid_size,obs,coin);
	double cost = rmap.getReward(player);
	std::cout<<"the cost is "<<cost<<std::endl;
	return 0;
}