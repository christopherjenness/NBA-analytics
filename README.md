# NBA-analytics
Short, offhand analyses of the NBA

## Topics Covered 
* James-Stein estimation of NBA statistics
* Player Efficiency Rating (PER)

## James-Stein estimation of NBA statistics (November 2016)
There is a very common problem after the first month of the NBA season.  How do you estimate someone's ability to shoot 3PT shots after they have taken there first 10 3PT attempts?  Maybe they only made 1, or maybe they made 9.  Either way, it seems unreasonable to use their current 3PT% as your best guess for what their 3PT% will be for the remainder of the season.

In fact, commentators frequently say things like, "He's currently shooting 55% from 3, but that should regress to the mean".  They don't really know what they are talking about, but there intuition is certainly correct.  The idea is that if a shooter begins shooting an extreme percentage, he is more likely to end up about average than maintain the extreme shooting for the rest of the seaon.

This is what James-Stein estimation tries to accomplish.  In frequentist statistics (Maximum likelihood estimation), you would assume every shooter's true 3PT% is whatever he is currently shooting.  However, James-Stein estimation says, actually, we need to dial it towards the league average.  Importantly, the extent to which we dial it back to the league average depends on how far from the mean the player is shooting and also how many shots the player has taken.  

So if a player is shooting 35% from 3 after taking 300 shots, James-Stein estimation will say he's probably about a 35% 3PT shooter.  On the other hand if a player is shooting 80% from 3, but has only taken 5 shots, James-Stein estimation will more say that players true 3PT% is much less than 80%.

In PER/PER.py we calculate the James-Stein estimated 3PT% for each player in the NBA using their 3PT shot data so far this season.  Details of the calculation can be found in:

Efron, Bradley, and Carl N. Morris. Stein's paradox in statistics. WH Freeman, 1977.

James-stein estimation is given by:

![Imgur](http://i.imgur.com/OTJUY8b.png)

where **y** is a vector of player's current 3PT% and the number of players m.  Notice how **y** is shrunk towards the origin.

![Imgur](http://i.imgur.com/F4PeD2n.png)

Here we have plotted the players emperical 3PT% (blue) and James-Stein 3PT% estimation (green).  As you can see, the extremes are dialed in towards the league average.

It also helps to look at individual cases.  J.J. Redick is a great 3PT shooter.  So far he is shooting 49%, making 34/69 shots.  Since he has taken a healthy amount of shots, James-Stein estimation only dials him back to 43%.  On the other hand, Serge Ibaka is also making nearly 49%, but only on 38 attempts.  James-Stein dials his 3PT% estimation all the way down to 37%.

Here are some interesting estimates of 3PT%:

![Imgur](http://i.imgur.com/tRxDD2Z.png)

## Player Efficiency Rating (PER)
