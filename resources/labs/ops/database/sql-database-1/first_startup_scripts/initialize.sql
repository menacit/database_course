-- SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
-- SPDX-License-Identifier: CC-BY-SA-4.0
-- X-Context: Database course - Operations lab - SQL script to setup database tables

-- WARNING: THIS SCRIPT IS ONLY EXECUTED ON INITIAL CREATION OF THE DATABASE!

-- Setup "missions" table
CREATE TABLE missions
    (id SERIAL PRIMARY KEY,
    submission_datetime TIMESTAMP, start_datetime TIMESTAMP, end_datetime TIMESTAMP,
    code_name TEXT, budget INTEGER, cost INTEGER, location_latitude TEXT, location_longitude TEXT,
    report_author TEXT, report TEXT);

-- Setup "participants" and "used_gadgets" tables
CREATE TABLE participants (id SERIAL PRIMARY KEY, mission_id INTEGER, name TEXT);
CREATE TABLE used_gadgets (id SERIAL PRIMARY KEY, mission_id INTEGER, name TEXT);

-- Create user account for "missions" application and assign privileges
CREATE ROLE db_app_user WITH LOGIN PASSWORD '0205Sopwith.Camel';

GRANT ALL ON
    missions, missions_id_seq,
    participants, participants_id_seq,
    used_gadgets, used_gadgets_id_seq
TO db_app_user;
