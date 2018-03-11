#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=print-statement
#
# Credits: TheSpace team from Melpignano

import os
import sys


class Ride:
    start_r = 0
    start_c = 0
    end_r = 0
    end_c = 0
    earliest_start = 0
    latest_finish = 0
    assigned = False
    index = -1

    def length(self):
        return abs(self.start_r - self.end_r) + abs(self.start_c - self.end_c)

    def __eq__(self, other):
        equal = self.start_r == other.start_r and self.start_c == other.start_c and \
            self.end_c == other.end_c and self.end_r == other.end_r and \
            self.earliest_start == other.earliest_start and self.latest_finish == other.latest_finish

        return equal

    def __ne__(self, other):
        return not self.__eq__(other)


class Car:
    next_r = 0
    next_c = 0
    __free_by_step = 0
    __earliest_start_bonus = 0

    def free_by_step(self):
        return self.__free_by_step

    def __init__(self, earliest_start_bonus):
        self.assigned_rides = []
        self.__earliest_start_bonus = earliest_start_bonus

    def assign_ride(self, ride):
        self.assigned_rides.append(ride.index)
        self.__free_by_step = self.__compute_free_by(ride)
        self.next_r = ride.end_r
        self.next_c = ride.end_c

    def __compute_free_by(self, ride):
        current_to_start_distance = self.__distance_to(ride.start_r, ride.start_c)
        wait_to_start_steps = ride.earliest_start - (self.__free_by_step + current_to_start_distance)
        if wait_to_start_steps < 0:
            wait_to_start_steps = 0
        travel_distance = ride.length()

        return self.__free_by_step + current_to_start_distance + wait_to_start_steps + travel_distance

    def __distance_to(self, r, c):
        return abs(self.next_r - r) + abs(self.next_c - c)

    def score_for_ride(self, ride):
        distance_from_my_next_stop_to_ride_start = self.__distance_to(ride.start_r, ride.start_c)
        arriving_to_ride_start_at = self.__free_by_step + distance_from_my_next_stop_to_ride_start
        if arriving_to_ride_start_at <= ride.earliest_start:
            bonus = self.__earliest_start_bonus
        else:
            bonus = 0
        arriving_to_ride_end_at = arriving_to_ride_start_at + ride.length()
        if arriving_to_ride_end_at < ride.latest_finish:
            score = bonus + ride.length()
        else:
            score = 0

        return score


class ProblemParser:
    def parse_problem(self, problem_statement):
        """Reads the input of a Self driving car problem.

        returns:
        R – number of rows of the grid ( 1 ≤ R ≤ 1 0000)
        C – number of columns of the grid ( 1 ≤ C ≤ 1 0000)
        F – number of vehicles in the fleet ( 1 ≤ F ≤ 1 000)
        N – number of rides ( 1 ≤ N ≤ 1 0000)
        B – per-ride bonus for starting the ride on time ( 1 ≤ B ≤ 1 0000)
        T – number of steps in the simulation ( 1 ≤ T ≤ 1 0 9 )
        rides –
            a – the row of the start intersection ( 0 ≤ a < R )
            b – the column of the start intersection ( 0 ≤ b < C )
            x – the row of the finish intersection ( 0 ≤ x < R )
            y – the column of the finish intersection ( 0 ≤ y < C )
            s – the earliest start ( 0 ≤ s < T )
            f – the latest finish ( 0 ≤ f ≤ T ) , ( f ≥ s + | x − a | + | y − b |)
        """
        lines = problem_statement.split("\n")
        R, C, F, N, B, T = [int(val) for val in lines[0].split()]
        rides = []
        
        for i in range(1, N + 1):
            ride = Ride()
            ride.start_r, ride.start_c, ride.end_r, ride.end_c, ride.earliest_start, ride.latest_finish = \
                [int(val) for val in lines[i].split()]
            ride.index = i - 1
            rides.append(ride)

        return R, C, F, N, B, T, rides


class ScoreSubmissionComputer:

    def compute(self, problem, submission):
        R, C, F, N, B, T, rides = ProblemParser().parse_problem(problem)

        total_score = 0
        submission_lines = submission.split("\n")
        for submission_line in submission_lines:
            submission_line_parts = map(int, submission_line.split())
            car = Car(B)
            if len(submission_line_parts) == 0:
                continue
            if len(submission_line_parts) != submission_line_parts[0] + 1:
                raise ValueError("Stated number of rides doesn't match the actual number of ride index")
            for ride_index in submission_line_parts[1:]:
                new_score = car.score_for_ride(rides[ride_index])
                car.assign_ride(rides[ride_index])
                if car.free_by_step() > T:
                    new_score = 0
                total_score = total_score + new_score

        return total_score
        

def main(argv):
    in_file_names = set()
    out_file_names = set()

    for file in os.listdir("files"):
        if file.endswith(".in"):
            in_file_names.add(file)
        if file.endswith(".out"):
            out_file_names.add(file)
    
    total_score = 0
    for in_file in in_file_names:
        out_file = in_file[:-3] + ".out"
        if out_file in out_file_names:
            problem = open("files/" + in_file).read()
            submission = open("files/" + out_file).read()
            score = ScoreSubmissionComputer().compute(problem, submission)
            total_score = total_score + score
            print("Score: " + str(score) + " for file: " + in_file)
    print ("\n Total score: " + str(total_score))
    
if __name__ == '__main__':
    main(sys.argv)