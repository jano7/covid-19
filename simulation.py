import matplotlib.pyplot as plt
import person
from person import Person
from matplotlib.ticker import FormatStrFormatter

r0 = 1.25
latent_period = 2
communicability = 10
hospitalization_rate = 0.04
hospitalization_period = 10
hospital_death_rate = 0.2
population_size = 66000000
number_of_beds = 115000

scaling_factor = 20
population_size /= scaling_factor
number_of_beds /= scaling_factor

print("Initializing ...")

people = []
while population_size > 0:
    people.append(
        Person(r0, latent_period, communicability, hospitalization_rate, hospitalization_period, hospital_death_rate))
    population_size -= 1

people[0].health = person.INFECTED
previously_infected = [people[0]]

print("Initialization completed")

infected_counts = []
hospitalized_counts = []
hospital_bed_counts = []
daily_deaths_counts = []
avoidable_deaths = 0
days = []
day = 1
while True:
    infected_people = []
    infected = 0
    hospitalized = 0
    daily_deaths = 0
    for p in previously_infected:
        yesterday_health = p.health
        health = p.live_day(day, people, infected_people)
        if (health == person.INFECTED) | (health == person.SEVERELY_ILL):
            if (health == person.SEVERELY_ILL) & (number_of_beds <= hospitalized):
                # assumption: a person not admitted to hospital dies
                p.health = person.DEAD
                avoidable_deaths += 1
                daily_deaths += 1
            else:
                infected_people.append(p)
                infected += 1
                if health == person.SEVERELY_ILL:
                    hospitalized += 1
        elif (health == person.DEAD) & (yesterday_health != person.DEAD):
            daily_deaths += 1

    infected_counts.append(infected * scaling_factor)
    hospital_bed_counts.append(number_of_beds * scaling_factor)
    hospitalized_counts.append(hospitalized * scaling_factor)
    daily_deaths_counts.append(daily_deaths * scaling_factor)
    days.append(day)
    print(f"day {day}: {infected * scaling_factor} infected, " +
          f"{hospitalized * scaling_factor} hospitalized, " +
          f"{daily_deaths * scaling_factor} daily deaths")
    if infected == 0:
        break
    previously_infected = infected_people.copy()
    day += 1

total_deaths = 0
for p in people:
    if p.health == person.DEAD:
        total_deaths += 1

not_infected = 0
for p in people:
    if p.health == person.NOT_INFECTED:
        not_infected += 1

print(f"{(not_infected / len(people)) * 100}% not infected")

fig, ax = plt.subplots()
ax.set_yscale('log')
ax.get_yaxis().set_major_formatter(FormatStrFormatter("%d"))
ax.set_xlabel("Day")
ax.set_ylabel("Population")
ax.plot(days, hospital_bed_counts, 'g--', label='Hospital Beds')
ax.plot(days, infected_counts, 'b-', label='Infected')
ax.plot(days, hospitalized_counts, 'r-', label='Hospitalized')
ax.plot(days, daily_deaths_counts, 'k-', label='Daily Deaths')
ax.legend()
plt.title(f"COVID-19 R0={r0}\n{total_deaths * scaling_factor} Total Deaths, " +
          f"{avoidable_deaths * scaling_factor} Avoidable Deaths")
plt.show()
