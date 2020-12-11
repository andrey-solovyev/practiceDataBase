from __init__ import *


def get_available_building():
    construction_positions = db.engine.execute(
        f'select * from construction_position').fetchall()
    return construction_positions


def get_type_building():
    construction_positions = db.engine.execute(
        f'select * from type_building').fetchall()
    return construction_positions


def get_available_flat_in_construction_position(id):
    flats = db.engine.execute(
        f"""SELECT * FROM flat AS f WHERE NOT EXISTS(SELECT * FROM contract AS c WHERE c.flat_id = f.id) and construction_id = {id} ORDER BY number_flat""").fetchall()
    return flats


def get_construction_by_position(id):
    construction = db.engine.execute(
        f"""SELECT * FROM construction AS f WHERE position_id = {id}""").fetchone()
    return construction


def get_construction_position(id):
    construction = db.engine.execute(
        f"""SELECT * FROM construction_position AS f WHERE id = {id}""").fetchone()
    return construction


def generate_flats(id):
    db.engine.execute(
        f"""DO
    $do$
        BEGIN
            FOR i IN 1..((SELECT number_of_flats FROM construction WHERE id = {id}) - 1)
                LOOP
                    INSERT INTO Flat (construction_id, number_flat, count_flat) VALUES (1, i, i / 4);
                END LOOP;
        END
$do$""")
