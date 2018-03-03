#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=print-statement
#
# Credits: TheSpace team from Melpignano

import tqdm
from random import randint
import matplotlib.pyplot as plt
import numpy as np
import sympy
from random import shuffle


class Ride:
    start_r = 0
    start_c = 0
    end_r = 0
    end_c = 0
    earliest_start = 0
    latest_finish = 0
    assigned = False
    index = -1

    def distance(self):
        return abs(self.start_r - self.end_r) + abs(self.start_c - self.end_c)


class Car:
    next_r = 0
    next_c = 0
    free_by_step = 0

    def __init__(self):
        self.assigned_rides = []

    def assign_ride(self, ride):
        self.assigned_rides.append(ride.index)
        self.next_r = ride.end_r
        self.next_c = ride.end_c
        self.free_by_step = self.__compute_free_by(ride)

    def __compute_free_by(self, ride):
        current_to_start_distance = self.__distance_to(ride.start_r, ride.start_c)
        wait_to_start_steps = ride.earliest_start - (self.free_by_step + current_to_start_distance)
        if wait_to_start_steps < 0:
            wait_to_start_steps = 0
        travel_distance = ride.distance()

        return current_to_start_distance + wait_to_start_steps + travel_distance

    def __distance_to(self, r, c):
        return abs(self.next_r - r) + abs(self.next_c - c)


def read_input_self_driving_data(filename):
    """Reads the input of a Self driving car problem.

    returns:
    R – number of rows of the grid ( 1 ≤ R ≤ 1 0000)
    C – number of columns of the grid ( 1 ≤ C ≤ 1 0000)
    F – number of vehicles in the fleet ( 1 ≤ F ≤ 1 000)
    N – number of rides ( 1 ≤ N ≤ 1 0000)
    B – per-ride bonus for starting the ride on time ( 1 ≤ B ≤ 1 0000)
    T – number of steps in the simulation ( 1 ≤ T ≤ 1 0 9 )
    city - a – the row of the start intersection ( 0 ≤ a < R )
        b – the column of the start intersection ( 0 ≤ b < C )
        x – the row of the finish intersection ( 0 ≤ x < R )
        y – the column of the finish intersection ( 0 ≤ y < C )
        s – the earliest start ( 0 ≤ s < T )
        f – the latest finish ( 0 ≤ f ≤ T ) , ( f ≥ s + | x − a | + | y − b |)
    """
    lines = open(filename).readlines()
    R, C, F, N, B, T = [int(val) for val in lines[0].split()]
    city = []
    
    for i in range(1, N + 1):
        ride = Ride()
        ride.start_r, ride.start_c, ride.end_r, ride.end_c, ride.earliest_start, ride.latest_finish = \
            [int(val) for val in lines[i].split()]
        ride.index = i - 1
        city.append(ride)

    return R, C, F, N, B, T, city

def build_cars(number_of_cars):
    cars = []
    for i in range(0, number_of_cars):
        car = Car()
        cars.append(car)
    
    return cars


def assign_rides_to_cars(filename):
    R, C, F, N, B, T, rides = read_input_self_driving_data(filename)
    cars = build_cars(F)

    rides.sort(key = lambda ride: ride.earliest_start)

    car_index = 0
    for ride in rides:
        cars[car_index].assign_ride(ride)
        car_index = car_index + 1
        if car_index == len(cars):
            car_index = 0 
    
    return cars


def write_output_assignements(filename, cars):
    """Writes an output file with the required format."""
    with open(filename, 'w') as f:
        for i in range(len(cars)):
            assigned_rides = cars[i].assigned_rides
            assigned_rides_indexes = " ".join(map(str, assigned_rides))
            f.write(str(len(assigned_rides)) + " " + assigned_rides_indexes + "\n")


cars = assign_rides_to_cars('files/a_example.in')
write_output_assignements('files/a_example.out', cars)
print('files/a_example.out')

cars = assign_rides_to_cars('files/b_should_be_easy.in')
write_output_assignements('files/b_should_be_easy.out', cars)
print('files/b_should_be_easy.out')

cars = assign_rides_to_cars('files/c_no_hurry.in')
write_output_assignements('files/c_no_hurry.out', cars)
print('files/c_no_hurry.out')

cars = assign_rides_to_cars('files/d_metropolis.in')
write_output_assignements('files/d_metropolis.out', cars)
print('files/d_metropolis.out')

cars = assign_rides_to_cars('files/e_high_bonus.in')
write_output_assignements('files/e_high_bonus.out', cars)
print('files/e_high_bonus.out')