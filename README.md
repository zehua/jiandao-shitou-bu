An implementation of Paper Scissor Stone in Python, for fun.

# Instructions

* Install Python 3
* run `./run` script with the number of rounds
```
./run 3
```
* run `make test` to run the tests

# Implemented

* human player from console
* ascii art rendering for hands and results
* computer player extensible with different strategies
* sample computer strategies (constant, random, composite robin robin strategy)

# Design Considerations

## Player centric view

I have chosen to design the views from the player's point of view instead of of from that of the overall game.

The overall game view might be useful when we want to support non-players viewing the games.

I think the player centric view could be designed as a sub-class of game centric view.

## Simultaneous playing (TODO)

* human trusts the program?
  * once human enters input, generate computer input without using human input
* human does not trust the program
  * use another program as judge
  * human and computer players both send input to the judge
* human vs human
  * as long as we could separate the player view for the two players, it would work.
  * the game controller runs on a different

## Player interactions as IO operations (TODO)

The `play` and `announce` actions from players are currently not explicitly captured as IO operations, as the computer one seems to not require any human interaction and is fast.

However, it is probably a lot cleaner to assume all player actions are IO, since a more complicated strategy might take a long time to produce an answer (think Deep Blue, Alpha Go).

By always considering the player actions as IO operations, it allows us to mark them as `async` and makes it a lot easier to convert the whole thing into an architecture that supports Web UI.

## Supporting Web UI (TODO)

How do we extend this design to support Web UI instead of Console based UI?

* UI driven vs flow driven
* current controller is flow driven
* if we adopt a continuation passing style web framework, we could continue with this, and change all the view hook functions to `async`
* otherwise, we will split the game controller into multiple steps, with the logic between each view hook as one step

# TODO

* error handling
  * too many failed attempts to enter input -> restart hand
  * too many draws -> consider it as a draw?
* style check pep8
* implement a strategy that makes use of recorded history
* script to compare performance of strategies (computer vs computer)
* support web UI
