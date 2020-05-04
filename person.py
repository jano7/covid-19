import math
import numpy as np
import sample as s

NOT_INFECTED = "not infected"
INFECTED = "infected"
SEVERELY_ILL = "severely ill"
IMMUNE = "immune"
DEAD = "dead"


class Person:
    def __init__(self, r0, latent_period, communicability, hospitalization_rate, hospitalization_period,
                 hospital_death_rate):
        self.infected_at_day = -1
        self.illness_day = 0
        self.health = NOT_INFECTED
        self.infection_non_hospital_days = s.latent_period_days_sample(latent_period)
        for day in s.person_spread_infection_days_sample(s.person_infects_others_sample(r0), communicability):
            self.infection_non_hospital_days.append(day)
        if s.hospitalization_sample(hospitalization_rate):
            self.hospital_days_count = s.hospitalization_period_sample(hospitalization_period)
            self.die_in_hospital = s.hospital_death_sample(hospital_death_rate)
        else:
            self.hospital_days_count = 0
            self.die_in_hospital = False

    def live_day(self, day, people, infected):
        if ((self.health == INFECTED) | (self.health == SEVERELY_ILL)) & (day > self.infected_at_day):
            self.illness_day += 1
            if self.illness_day > len(self.infection_non_hospital_days):
                if self.hospital_days_count > 0:
                    # assumption: a person in hospital does not spread infection
                    self.health = SEVERELY_ILL
                    self.hospital_days_count -= 1
                else:
                    if self.die_in_hospital:
                        self.health = DEAD
                    else:
                        self.health = IMMUNE
            else:
                meet_people_count = self.infection_non_hospital_days[self.illness_day - 1]
                # spread the infection
                while meet_people_count > 0:
                    p = people[math.floor(np.random.random() * len(people))]
                    if p.meet_infected(day):
                        infected.append(p)
                    meet_people_count -= 1
        return self.health

    def meet_infected(self, day):
        if self.health == NOT_INFECTED:
            self.infected_at_day = day
            self.health = INFECTED
            return True
        return False
