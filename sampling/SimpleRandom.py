from django.db import models
import math


# confidence interval
# margin of error
# population size
# sample size

def zscorecalculator(ci):
    match ci:
        case 80:
            return 1.28
        case 85:
            return 1.44
        case 90:
            return 1.65
        case 95:
            return 1.96
        case 99:
            return 2.58


class SimpleRandom:
    def __init__(self,margin_of_error,confidence_level, individuals, households, non_response_rate, subgroups):
        self.margin_of_error = margin_of_error
        self.confidence_level = confidence_level
        self.non_response_rate = non_response_rate
        self.subgroups = subgroups
        self.individuals = individuals
        self.households = households

        if margin_of_error is None:
            raise ValueError("margin_of_error cannot be None")
        if margin_of_error == 0:
            raise ValueError("margin_of_error cannot be zero")
        if confidence_level is None:
            raise ValueError("confidence_level cannot be None")
        if non_response_rate is None:
            raise ValueError("non_response_rate cannot be None")

        if individuals or households:
            self.individuals = individuals
            self.households = households
            if individuals:
                self.population_size = individuals
            else:
                self.population_size = households * 4  # assumed the average number of people in a single household = 4

        if subgroups is None:
            self.sample_size = self.calculate_sample_size(self.population_size, self.margin_of_error,
                                                          self.confidence_level, self.non_response_rate)
            # print("######################")
        else:
            self.sample_size = self.calculate_subgroup_sample_sizes(self.margin_of_error,
                                                                    self.confidence_level, self.non_response_rate,
                                                                    self.subgroups)

    def calculate_sample_size(self, population_size, margin_of_error, confidence_level, non_response_rate):

        z = zscorecalculator(confidence_level)
        numerator = (z * z * 0.5 * 0.5) / (margin_of_error * margin_of_error * 0.01 * 0.01)
        # print(numerator)
        denominator = 1 + (numerator / population_size)
        # print(denominator)
        ans = numerator / denominator
        sample_size = ans / (1 - (non_response_rate / 100))
        return math.ceil(sample_size)

    # Stratified Random Sampling
    def calculate_subgroup_sample_sizes(self, margin_of_error, confidence_level, non_response_rate,
                                        subgroups):
        result = []
        # Format of subgroups : [{'name':'a','size':100},{'name':'b','size':200}]
        for i in subgroups:
            # print(i)
            ans = self.calculate_sample_size(i['size'], margin_of_error, confidence_level, non_response_rate)
            result.append(ans)
        cumulative_sample_size = sum(result)
        result.append(cumulative_sample_size)
        # format of result : [sample_size_subgroup1,sample_size_subgroup2....,cumulative_sample_size]
        print(result)
        return math.ceil(cumulative_sample_size)

    def get_sample_size(self):
        return self.sample_size

# if __name__ == '__main__':
#     simpleRandom = SimpleRandom(margin_of_error=5, confidence_level=95, individuals=100, households=0,
#                                 non_response_rate=0, subgroups=None)
#     # simple_random = SimpleRandom(0.05,95,100,0,5,0)
#     # print(simple_random)
#     sample_size = simpleRandom.get_sample_size()
#     print(sample_size)
