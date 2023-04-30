
import LightsOut
import utils
import time

GRID_HEIGHT = 5
GRID_LENGTH = 5

class Transform:
    def __init__(self, condition, output, overlap=False):
        self.condition = condition
        self.output = output
        self.overlap = overlap

    def getSimilarity(self, condition):
        checks, correct = 0, 0
        aoe = utils.areaOfEffect(self.output)
        for y in range(GRID_HEIGHT):
            for x in range(GRID_LENGTH):
                if aoe[y][x]:
                    checks += 1
                    if self.condition[y][x] == condition[y][x]:
                        correct += 1
        return correct / checks
    
    def __str__(self):
        return utils.ruleToString(self.condition, self.output)

class Rule:
    def __init__(self, condition, output):
        self.condition = condition
        self.output = output
        self.transforms = [Transform(transform[0], transform[1]) for transform in utils.getTransforms(condition, output)]
        
    def getBestNTransforms(self, condition, n):
        self.transforms.sort(key=lambda transform: transform.getSimilarity(condition), reverse=True)
        return [self.transforms[i] for i in range(n)]

    def __str__(self):
        return utils.ruleToString(self.condition, self.output)
    
class Ruleset:
    def __init__(self):
        self.rule_set = [Rule(
            [
                [0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
            ],
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ]
        )]

    def getBestNTransforms(self, condition, n):
        transforms = []
        for rule in self.rule_set:
            best_n_transforms = rule.getBestNTransforms(condition, n)
            for transform in best_n_transforms:
                transforms.append(transform)
        transforms.sort(key=lambda transform: transform.getSimilarity(condition), reverse=True)
        return transforms

    def maxAttempts(self, max_breadth, max_depth):
        max_attempts = 0
        for i in range(1, max_depth+1):
            max_attempts += max_breadth**i
        return max_attempts

    def isOverlap(self, condition1, condition2):
        return utils.matrixXOR(condition1, condition2) != utils.matrixOR(condition1, condition2)

    def getNextTransformCombo(self, transform_combo, transform):
        overlap = self.isOverlap(transform_combo.condition, transform.condition)
        return Transform(utils.matrixXOR(transform_combo.condition, transform.condition), utils.matrixXOR(transform_combo.output, transform.output), overlap)

    # max_n_attempts = max_b^1 + max_b^2 + ... + max_b^max_d
    def solve(self, config, max_breadth=2, max_depth=2):
        max_attempts = self.maxAttempts(max_breadth * len(self.rule_set), max_depth)
        transform_combos = [Transform(utils.getNullMatrix(), utils.getNullMatrix())]
        for transform_combo in transform_combos:
            next_config = utils.matrixXOR(config, transform_combo.condition)
            next_transforms = self.getBestNTransforms(next_config, max_breadth)
            for transform in next_transforms:
                next_transform_combo = Transform(utils.matrixXOR(transform_combo.condition, transform.condition), utils.matrixXOR(transform_combo.output, transform.output))
                if next_transform_combo.condition == config:
                    print(f'solved in {len(transform_combos)-1} attempts!')
                    return next_transform_combo.output
                if len(transform_combos) > max_attempts:
                    print(f'unable to solve in {max_attempts} attempts.')
                    return None
                transform_combos.append(next_transform_combo)

    # learn new rules by config difficulty
    def train(self, config, max_breadth_per_rule=2, max_depth=2):
        max_attempts = self.maxAttempts(max_breadth_per_rule * len(self.rule_set), max_depth)
        transform_combos = [Transform(utils.getNullMatrix(), utils.getNullMatrix())]
        for transform_combo in transform_combos:
            next_config = utils.matrixXOR(config, transform_combo.condition)
            next_transforms = self.getBestNTransforms(next_config, max_breadth_per_rule)
            for transform in next_transforms:
                next_transform_combo = Transform(utils.matrixXOR(transform_combo.condition, transform.condition), utils.matrixXOR(transform_combo.output, transform.output))
                if next_transform_combo.condition == config:
                    if len(transform_combos)-1 > max_attempts / 2:
                        new_output = utils.toCenter(next_transform_combo.output)
                        new_condition = utils.listToMatrix(LightsOut.genStartingConfig(utils.matrixToList(new_output)))
                        new_rule = Rule(new_condition, new_output)
                        self.rule_set.append(new_rule)
                    return True
                if len(transform_combos) > max_attempts:
                    return None
                transform_combos.append(next_transform_combo)

    # learn new rules by pattern overlaps
    def train2(self, config, max_breadth_per_rule=2, max_depth=2):
        max_attempts = self.maxAttempts(max_breadth_per_rule * len(self.rule_set), max_depth)
        transform_combos = [Transform(utils.getNullMatrix(), utils.getNullMatrix())]
        for transform_combo in transform_combos:
            next_config = utils.matrixXOR(config, transform_combo.condition)
            next_transforms = self.getBestNTransforms(next_config, max_breadth_per_rule)
            for transform in next_transforms:
                next_transform_combo = self.getNextTransformCombo(transform_combo, transform)
                if next_transform_combo.condition == config:
                    if next_transform_combo.overlap:
                        new_output = utils.toCenter(next_transform_combo.output)
                        new_condition = utils.listToMatrix(LightsOut.genStartingConfig(utils.matrixToList(new_output)))
                        new_rule = Rule(new_condition, new_output)
                        self.rule_set.append(new_rule)
                    return True
                if len(transform_combos) > max_attempts:
                    return None
                transform_combos.append(next_transform_combo)

    def __str__(self):
        return '\n'.join([str(rule) for rule in self.rule_set])

ruleset = Ruleset()
for d in range(10):
    n_iterations = 25*(d+1)
    print(f'Training on difficulty {d+1} for {n_iterations} iterations...')
    n_rules_before_training = len(ruleset.rule_set)
    n_correct = 0
    for i in range(n_iterations):
        config = utils.listToMatrix(LightsOut.genStartingConfig(LightsOut.genSolution(d+1)))
        if ruleset.train2(config):
            n_correct += 1
    print(f'    Completed with {(n_correct / n_iterations) * 100:.0f}% success rate.')
    print(f'    Learnt {len(ruleset.rule_set) - n_rules_before_training} new rules.')
    print(f'    Total {len(ruleset.rule_set)} rules.')
