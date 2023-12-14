s = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

data = s.split('\n')

def parse_data(data: "list[str]") -> "list[tuple[str, tuple[int]]]":
    new_data = []
    for line in data:
        springs, damaged = line.split(' ')
        damaged = tuple([int(x) for x in damaged.split(',')])
        new_data.append((springs, damaged))
    return new_data

parsed = parse_data(data)

print(parsed)

#https://www.reddit.com/r/adventofcode/comments/18hbbxe/2023_day_12python_stepbystep_tutorial_with_bonus/

"""Plan on how to solve P1 below. Sorry for the messy spoiler tags, yay for Reddit formatting. To try and be clear, this solution is pretty sub-optimal, but it should be enough to get going on P1.

Let's make a little plan to solve this.

Say we create an array with one string we would like to check: [".#?#? 3"]

We first want to see what possibilities are hiding inside this string. This means replacing the ? with a . or a #, per the instructions. Both options can be true.

Get the first string from the array, remove it from the array and:

-> Scan the first character.

-> If the character is a . or a #, continue to the next character.

-> If the character is a ?, create a new string where you replace this character with a "#", create another new string where you replace this character with a ".". This string is now finished, grab the next one from the array.

-> If the end of the string is reached, add to a new "result" array.

So after the first pass the array now looks like this:

[".#.#? 3", ".###? 3"]

If you repeat the above process for all the strings containing question marks, you end up with a result array containing all possible configurations for the values you originally input.

Now, for each of these values, you need to test against the rules. Groups need to match the springs. So:

-> Set active group

-> Start counting when you find the first #

-> When you hit a dot, check if you are counting (see above), and see if your count is your active group.

-> Yes? Move onto next group, if there is any. Your count is 0 again.

-> No? This state is not valid! Prune.

-> When you hit a #, add 1 to your count, check if there is an active group (no? prune!), check if you are not above the current active group value (above? prune!)

-> No more string left? Check if the count == activegroup, or count == 0 and there no activegroup. (Protip: If you add a "." to all input strings, you do not need specific logic for this)

Walking through all the unpacked strings and checking against the rules should give you a total number of "correct" strings. P1 solved!"""