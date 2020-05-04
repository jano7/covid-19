import numpy as np
import math


def person_infects_others_sample(r0):
    return np.random.binomial(r0 * 100, .01)


def person_spread_infection_days_sample(infected_people_count, communicability):
    infect_at_days = {}
    for i in np.random.random(infected_people_count):
        day = math.floor(communicability * i)
        if day in infect_at_days:
            infect_at_days[day] += 1
        else:
            infect_at_days[day] = 1
    days = []
    day = 0
    while day < communicability:
        if day in infect_at_days:
            days.append(infect_at_days[day])
        else:
            days.append(0)
        day += 1
    return days


def hospital_death_sample(hospital_death_rate):
    return np.random.random() < hospital_death_rate


def hospitalization_period_sample(hospitalization_period):
    if hospitalization_period <= 1:
        raise Exception("latent_period has to be > 1")
    return 1 + np.random.binomial((hospitalization_period - 1) * 100, .01)


def hospitalization_sample(hospitalization_rate):
    return np.random.random() < hospitalization_rate


def latent_period_days_sample(latent_period):
    if latent_period <= 1:
        raise Exception("latent_period has to be > 1")
    i = 1 + np.random.binomial((latent_period - 1) * 100, .01)
    latent_period_days = []
    while i > 0:
        latent_period_days.append(0)
        i -= 1
    return latent_period_days
