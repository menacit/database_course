# SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
# SPDX-License-Identifier: CC-BY-SA-4.0
# X-Context: Database course - Pony ORM demo application
from pony.orm import *

db = Database()

class Agent(db.Entity):
    name = Required(str)
    code_name = Optional(str, unique=True)
    salary = Required(int)
    gadgets = Set('Gadget')
    missions = Set('Mission')

class Gadget(db.Entity):
    name = Required(str)
    price = Required(int)
    owner = Optional(Agent)

class Mission(db.Entity):
    code_name = Required(str)
    participants = Set(Agent)

db.bind(
    provider='sqlite',
    filename=':sharedmemory:')

set_sql_debug(True)
db.generate_mapping(
    create_tables=True)

with db_session:
    spy_watch = Gadget(
        name='Omicron Spymaster watch',
        price=92500) 
    
    madam = Agent(
        name='Malory Archer',
        code_name='Madam', salary=55000)
    
    duchess = Agent(
        name='Sterling Archer',
        code_name='Duchess', salary=42000)
    
    theft_mission = Mission(
        code_name='Cracked Meatball')
    
    duchess.gadgets.add(spy_watch)
    theft_mission.participants.add(duchess)

with db_session:
    print(Agent.get(code_name='Madam').name)

    for gadget in Agent.get(
        code_name='Duchess').gadgets:

        print(gadget.name)

    for name in select(a.name for a in Agent):
        print(name)

    for expensive_agent in select(
        a for a in Agent
            if a.salary > 8000 and
            a.name != 'Malory Archer' ):

        print(expensive_agent.name)
        expensive_agent.salary -= 1000
