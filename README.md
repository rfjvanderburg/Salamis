# Salamis

Salamis is a turn-based strategy game for 2 players, which goal is to destroy all ships of the other player. The game is currently largely text-based, awaiting an API to be implemented. 

## Gameplay

The game starts with 10 islands that are randomly placed (but such that the starting conditions are fairly balanced between the players) on a map. Each island is either onoccupied, or held by either of the players. Each island has a certain *value*, which is the number of ships received by the player holding the island, at the end of the turn. 

The two players (blue and red) each start with one island (with value 10) and 10 ships. From there they can send ships to conquer other islands. Onoccupied islands can be taken with a number a ships that exceeds the *value* of the island. So, for example, to take an onoccupied island of value 6, at least 7 ships need to arrive at the island. 


Ships have a set but finite speed and thus take a certain number of turns to sail to other islands. Ships that are sailing can only be tracked by the player that owns those ships, while all stationary ships (i.e. after they have arrived at an island) can be seen by both players. Sailing plans can never be changed; boats will always continue their journey until their set destination.

When two players arrive at an island at the same turn, a sea battle proceeds before any of the fleets make it to the island. Sea battles are fair - there is no advantage to the defending party. When defending an island against another player, a "defending bonus" is in place, default factor being *1.25*. Four defending ships are then counted as five.

Once one of the players, at the end of a certain round, has no ships left (either stationary or sailing), the other players has won the game.

Several parameters are tunable to change the Gameplay:
-Number of islands
-Speed of ships
-Magnitude of defense bonus
