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

def get_construction_positions():
    construction = db.engine.execute(
        f"""SELECT * FROM construction_position AS f """).fetchall()
    return construction

def get_all_humans():
    construction = db.engine.execute(
        f"""SELECT id, surname ||' '|| name ||' '|| middle_name as full_name FROM human AS f""").fetchall()
    return construction


def insert_new_human(surname, name, middle_name, inputDate, passport_data, address, phone):
    db.engine.execute(
        f'INSERT INTO human (surname, name, middle_name, date_of_birth, passport_data, residence_address, phone) VALUES (%s,%s, %s, %s,%s,%s,%s)',
        (surname, name, middle_name, inputDate, passport_data, address, phone,))


def get_count_available_flat_in_construction_position(id):
    flats = db.engine.execute(
        f"""SELECT COUNT(*) FROM flat AS f WHERE NOT EXISTS(SELECT * FROM contract AS c WHERE c.flat_id = f.id) and construction_id = {id}""").fetchone()
    return flats


def get_count_flats(id):
    flats = db.engine.execute(
        f"""SELECT f.count_flat,COUNT(f.number_flat) FROM Flat AS f WHERE f.construction_id={id} GROUP BY f.count_flat ORDER BY f.count_flat""").fetchall()
    return flats




#  ПОИСК
def get_performance_by_title(name):
    performances = db.engine.execute(
        f"""SELECT id,Date,q.title FROM performance AS p JOIN Production AS q ON Production.id=q.production_id WHERE LOWER({name}) IN LOWER(q.title) """).fetchall()
    return performances
def get_performance_by_title_and_date(name,date):
    performances = db.engine.execute(
        f"""SELECT p.id,p.Date,q.title FROM performance AS p JOIN Production AS q ON Production.id=q.production_id WHERE LOWER({name}) IN LOWER(q.title) OR  p.date = CAST({date} AS DATE)""").fetchall()
    return performances
#  КОНЕЦ ПОИСКа




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
