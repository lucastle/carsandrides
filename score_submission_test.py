#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import sys
from score_submission import ScoreSubmissionComputer, Ride, ProblemParser

class TestProblemParser(unittest.TestCase):
    def test_parse_problem(self):
        problem = "2 2 1 1 0 3\n0 0 1 1 0 2"
        parsed_settings = [2, 2, 1, 1, 0, 3]
        parsed_ride = Ride()
        parsed_ride.start_r = 0
        parsed_ride.start_c = 0
        parsed_ride.end_r = 1
        parsed_ride.end_c = 1
        parsed_ride.earliest_start = 0
        parsed_ride.latest_finish = 2
        R, C, F, N, B, T, rides = ProblemParser().parse_problem(problem)
        self.assertEquals(parsed_settings, [R, C, F, N, B, T])
        self.assertEquals(parsed_ride, rides[0])



class TestScoreSubmission(unittest.TestCase):

    def test_score_empty_line_submissions(self):
        problem = "2 2 1 1 0 3\n0 0 1 1 0 2"
        submission = "1 0\n"
        ScoreSubmissionComputer().compute(problem, submission)

    def test_score_incorrect_ride_number(self):
        problem = "2 2 1 1 0 3\n0 0 1 1 0 2"
        submission = "1 0 0"
        try:
            score = ScoreSubmissionComputer().compute(problem, submission)
        except ValueError:
            return
        self.fail("Unexpected non raised exception")

    def test_score_trivial_case(self):
        problem = "2 2 1 1 0 3\n0 0 1 1 0 3"
        submission = "1 0"
        score = ScoreSubmissionComputer().compute(problem, submission)
        self.assertEquals(score, 2)

    def test_score_trivial_case_late(self):
        problem = "2 2 1 1 0 3\n0 0 1 1 0 1"
        submission = "1 0"
        score = ScoreSubmissionComputer().compute(problem, submission)
        self.assertEquals(score, 0)

    def test_score_trivial_case_with_bonus(self):
        problem = "2 2 1 1 1 3\n0 0 1 1 0 3"
        submission = "1 0"
        score = ScoreSubmissionComputer().compute(problem, submission)
        self.assertEquals(score, 3)

    def test_score_trivial_case_after_the_end(self):
        problem = "2 2 1 1 1 1\n0 0 1 1 0 3"
        submission = "1 0"
        score = ScoreSubmissionComputer().compute(problem, submission)
        self.assertEquals(score, 0)      

    def test_score_example(self):
        problem = open("files/a_example.in").read()
        submission = open("score_submission_test_files/a_example_10.out").read()
        score = ScoreSubmissionComputer().compute(problem, submission)
        self.assertEquals(score, 10)

    def test_score_should_be_easy(self):
        problem = open("files/b_should_be_easy.in").read()
        submission = open("score_submission_test_files/b_should_be_easy_176877.out").read()
        score = ScoreSubmissionComputer().compute(problem, submission)
        self.assertEquals(score, 176877) 

    def test_score_no_hurry(self):
        problem = open("files/c_no_hurry.in").read()
        submission = open("score_submission_test_files/c_no_hurry_8130306.out").read()
        score = ScoreSubmissionComputer().compute(problem, submission)
        self.assertEquals(score, 8130306)

    def test_score_metropolis(self):
        problem = open("files/d_metropolis.in").read()
        submission = open("score_submission_test_files/d_metropolis_8349276.out").read()
        score = ScoreSubmissionComputer().compute(problem, submission)
        self.assertEquals(score, 8349276)

    def test_score_high_bonus(self):
        problem = open("files/e_high_bonus.in").read()
        submission = open("score_submission_test_files/e_high_bonus_21465945.out").read()
        score = ScoreSubmissionComputer().compute(problem, submission)
        self.assertEquals(score, 21465945)         

def main(argv):
    unittest.main()

    
if __name__ == '__main__':
    main(sys.argv)