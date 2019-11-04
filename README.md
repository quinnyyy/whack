# Whack (Built for Wellsley Hacks)
**An online multiplayer block pushing game**

## Inspiration
We wanted to make a .io style game (think agar.io). At first we couldn't think of any ideas but then we spotted a wheeled trash can across the venue and we knew that we wanted to make a game where you push trash cans into other people to kill them.

## What it does
You play in a 2D map against other players. Trash cans are randomly spawned and you can push them into other players. You get points when hitting others.

## How we built it
We use a flask backend to implement the game logic. We use a javascript frontend (no frameworks) to paint an html canvas based on the game state and to display the scores of players. We communicate between the backend and frontend using websockets using socket.io.

We are currently in the process of hosting on AWS EC2 with Apache (its a struggle)

## Challenges we ran into

Neither of us were very experienced with socket programming so there was some learning curve with that.
We also spent a lot of time trying to host on AWS with Apache and it turned out to be more difficult than anticipated.

## Accomplishments that we're proud of
We have a smooth game with all the game logic implemented and working (AFAIK)

## What we learned
We learned about socket programming and EC2 and Apache 

## What's next for WHACKER
We are going to put ads and become millionaires

## Tech Stack
Built with AWS EC2, Apache2, Javascript and Python (Flask)

## Links

[Play Here](https://tinyurl.com/y5g6s65j)

[Video](https://www.youtube.com/watch?v=-HZKKW8XfYI)

[Presentation](https://docs.google.com/presentation/d/1g0O3EkcpDhTwTSuROcJxAA1C-JPhf-3Sq8P1fYxNOrc/edit?usp=sharing)

[Devpost](https://devpost.com/software/whacker)
