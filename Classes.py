from __init__ import *
def get_available_building():
    construction_positions = db.engine.execute(
        f'select address,number from construction_position').fetchall()
    return construction_positions