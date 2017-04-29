#include "reward.hpp"

point operator-(point& a, point& b)
{
	// overloading the subraction operator for two points
	// returns a vector (mathematical) point from point b to point a 
	return point(a.x - b.x, a.y-b.y);
}

rewardmap::rewardmap(std::string& address, int& Grid , std::vector<point>& Obs,std::vector<point>& Coin):
				grid_size(Grid),obs(Obs),coin(Coin)
{
	// hardcoding the weights for feature values
	// should be read from a txt file in the final version

	alpha.push_back(-174.0);
	alpha.push_back(-174.0);
	alpha.push_back(300);
	alpha.push_back(400);

}

double rewardmap::getCost(point player)
{
	// get the reward of the input point 'player'
	std::vector<double> f_val(4,0);
	int sumD =0;
	int minD =INT_MAX;
	int dist = 0;
	for(int i = 0; i< obs.size();i++)
	{
		dist = obs[i].getMdistance(player);
		sumD += dist;
		if (dist < minD) minD = dist;
	}
	f_val[2] = minD/(grid_size*2.0);
	f_val[3] = sumD/(obs.size()*grid_size*2.0);
	
	sumD =0;
	minD =INT_MAX;
	dist = 0;
	
	for(int i = 0;i<coin.size();i++)
	{
		dist = coin[i].getMdistance(player);
		sumD += dist;
		if (dist < minD) minD = dist;
	}
	f_val[0] = minD/(grid_size*2.0);
	f_val[1] = sumD/(coin.size()*grid_size*2.0);

	return f_val[0]*alpha[0] + f_val[1]*alpha[1] + f_val[2]*alpha[2] + f_val[3]*alpha[3];
}

