import time
import os


class Policy:
    def __init__(self, n1: int, n2: int, letter: str):
        assert(n1 < n2)
        self.n1 = n1
        self.n2 = n2
        self.letter = letter


class Password:
    def __init__(self, policy: Policy, password: str):
        self.policy = policy
        self.password = password

    def validate_rule_1(self) -> bool:
        # Password should contain the letter at least n1 times and at most n2 times.
        count = self.password.count(self.policy.letter)
        return (count >= self.policy.n1) and (count <= self.policy.n2)
        # Why not do this?:
        #     return self.password.count(self.policy.letter) in range(self.policy.n1, self.policy.n2 + 1)
        # Put simply: it's slower. Which makes sense if you think about possible ways Python could implement the check.
        # That said, it's negligible at the size of the real input:
        # It was about about 2 seconds slower over 10,000 iterations of the entire input file.

    def validate_rule_2(self) -> bool:
        # Password should contain the letter in exactly 1 of locations n1 and n2.
        # We have to account for these passwords being 1-indexed in the policy.
        return (self.password[self.policy.n1 - 1] == self.policy.letter) \
            ^ (self.password[self.policy.n2 - 1] == self.policy.letter)  # ^ (xor) and != will give same result.


def parse_input(filename: str):
    passwords: list[Password] = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip().split(": ")
            policy = line[0].split(" ")
            policy_nums = policy[0].split("-")
            passwords.append(Password(Policy(int(policy_nums[0]), int(policy_nums[1]), policy[1]), line[1]))
    return passwords


def main(input_filename: str):
    if not os.path.exists(input_filename):
        raise FileNotFoundError(f"Couldn't find input file: {input_filename}")

    start_time = time.time()
    passwords = parse_input(input_filename)

    part1_start = time.time()
    passing_policy = 0
    for password in passwords:
        passing_policy += password.validate_rule_1()
    print(f"{passing_policy} passwords passed policy 1.")

    part2_start = time.time()
    passing_policy = 0
    for password in passwords:
        passing_policy += password.validate_rule_2()
    print(f"{passing_policy} passwords passed policy 2.")

    end_time = time.time()
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")
    return


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        filename = "../../inputs/2020/day02.txt"
        main(filename)

    run_main()
