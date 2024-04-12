-- SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
-- SPDX-License-Identifier: CC-BY-SA-4.0
-- X-Context: Database course - Security lab - SQL script to setup database tables

-- WARNING: THIS SCRIPT IS ONLY EXECUTED ON INITIAL CREATION OF THE DATABASE!

-- Setup "agents" table and default data
CREATE TABLE agents
    (id SERIAL PRIMARY KEY, name TEXT NOT NULL, code_name TEXT, salary INTEGER);

INSERT INTO agents (name, code_name, salary) VALUES
    ('Sterling Archer', 'Duchess', 42000),
    ('Lana Kane', 'Monster Hands', 42001),
    ('Cyril Figgis', 'Chokely Carmichael', 5500),
    ('Ray Gillette', 'Gilles de Rais', 26000),
    ('Malory Archer', 'Madam', 55000);

-- Setup "gadgets" table and default data
CREATE TABLE gadgets
    (id SERIAL PRIMARY KEY, name TEXT NOT NULL, price INTEGER NOT NULL);

INSERT INTO gadgets (name, price) VALUES
    ('Fake mustache', 5),
    ('Doplhin Puppet', 8),
    ('Magic breath strips', 50),
    ('Tactical cane', 4800),
    ('Mind control microchip (934-TX)', 71000),
    ('Omicron Spymaster watch', 92500);

-- Setup "gadget assignments" table and default data
CREATE TABLE gadget_assignments
(id SERIAL PRIMARY KEY, gadget_id INTEGER NOT NULL, agent_id INTEGER NOT NULL);

INSERT INTO gadget_assignments (gadget_id, agent_id) VALUES
    (1, 1), (2, 1), (6, 1), (6, 2), (2, 3), (7, 4);

-- Create shared application user/role
CREATE ROLE shared_app_user WITH LOGIN PASSWORD 'weshouldnotusethisaccount';

-- Grant all privileges to the "agency" database.
-- FYI: "Sequence tables" are automatically created for columns of "SERIAL" type
-- (<table_name>_<column_name>_seq). These sequence tables must also be writable
-- for updates to the "source table".
GRANT ALL ON
    agents, agents_id_seq,
    gadgets, gadgets_id_seq,
    gadget_assignments, gadget_assignments_id_seq
TO shared_app_user;
