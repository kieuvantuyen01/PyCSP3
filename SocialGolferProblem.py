from pycsp3 import *

def social_golfers():
    nGroups, size, nWeeks = data
    nPlayers = nGroups * size

    print(f"Social Golfer Problem with {nPlayers} players, {nGroups} groups of size {size} and {nWeeks} weeks")

    # x[w][p] is the group admitting on week w the player p
    x = VarArray(size=[nWeeks, nPlayers], dom=range(nGroups))

    satisfy(
        # ensuring that two players don't meet more than one time
        [
            If(
                x[w1][p1] == x[w1][p2],
                Then=x[w2][p1] != x[w2][p2]
            ) for w1, w2 in combinations(nWeeks, 2) for p1, p2 in combinations(nPlayers, 2)
        ],
        # respecting the size of the groups
        [Cardinality(x[w], occurrences={i: size for i in range(nGroups)})
            for w in range(nWeeks)],
        # tag(symmetry-breaking)
        LexIncreasing(x, matrix=True)
    )

    if solve() is SAT:
        for w in range(nWeeks):
            print("Groups of week ", w , [[p for p in range(nPlayers) if x[w][p].value == g] for g in range(nGroups)])

# Read data from file
for line in open("data.txt"):
    if line[0] != "#":
        data = [int(x) for x in line.split()]
        social_golfers()
