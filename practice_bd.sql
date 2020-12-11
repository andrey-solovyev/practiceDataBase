CREATE TABLE User_Site(
    Id SERIAL PRIMARY KEY,
    email CHARACTER VARYING(255),
    password_hash CHARACTER VARYING(255),
    role smallint default 0
);

CREATE TABLE Human(
	Id SERIAL PRIMARY KEY,
	surname CHARACTER VARYING(30),
	name CHARACTER VARYING(30),
	middle_name CHARACTER VARYING(30),
	date_of_birth TIMESTAMP,
	passport_data CHARACTER VARYING(255),
	residence_address CHARACTER VARYING(255),
	phone CHARACTER VARYING(30)
);

CREATE TABLE Construction_position(
	Id SERIAL PRIMARY KEY,
	number integer,
	address CHARACTER VARYING(255)
);
CREATE TABLE Construction(
	Id SERIAL PRIMARY KEY,
	position_id integer,
	type_build_id integer,
	date_fundament TIMESTAMP,
	number_of_flats integer,
	date_of_delivery timestamp,
	date_actual_delivery timestamp,
	heating bool,
	gas bool,
	FOREIGN KEY (position_id) REFERENCES Construction_position (Id) ON DELETE CASCADE
);

CREATE TABLE type_building(
    Id integer,
    material CHARACTER VARYING(30),
    FOREIGN KEY (Id) REFERENCES Construction (Id) ON DELETE CASCADE

);
CREATE TABLE Flat(
	Id SERIAL PRIMARY KEY,
	construction_id integer,
	number_flat integer,
	count_flat integer,
    FOREIGN KEY (construction_id) REFERENCES Construction (Id) ON DELETE CASCADE
);
CREATE TABLE Plan_floor(
    Id SERIAL PRIMARY KEY,
    construction_id integer,
    file_name CHARACTER VARYING(255),
    FOREIGN KEY (construction_id) REFERENCES Construction (Id) ON DELETE CASCADE
);

CREATE TABLE Stage(
    Id SERIAL PRIMARY KEY,
    construction_id integer,
    date_stage timestamp,
    description text,
    FOREIGN KEY (construction_id) REFERENCES Construction (Id) ON DELETE CASCADE
);


CREATE TABLE Contract(
	Id SERIAL PRIMARY KEY,
	human_id integer,
	flat_id integer,
	date_contract TIMESTAMP,
	surname_employee CHARACTER VARYING(255),
	downpayment float,
    FOREIGN KEY (human_id) REFERENCES Human (Id) ON DELETE CASCADE,
    FOREIGN KEY (flat_id) REFERENCES Flat (Id) ON DELETE CASCADE
);


with ta as (INSERT INTO construction_position (number, address) VALUES (1, 'Voronezh, new arbat street') RETURNING id)
INSERT
INTO Construction (position_id, date_fundament, number_of_flats, date_of_delivery, date_actual_delivery, heating, gas)
VALUES ((SELECT id FROM ta), '2020-10-06 10:56:16.310914', 168, '2021-10-06 10:56:16.310914', null, true, true);

INSERT INTO type_building (material)
VALUES ('Monolith');

DO
$do$
    BEGIN
        FOR i IN 1..((SELECT number_of_flats FROM construction WHERE id = 1) - 1)
            LOOP
                INSERT INTO Flat (construction_id, number_flat, count_flat) VALUES (1, i, i / 4);
            END LOOP;
    END
$do$;

INSERT INTO human (surname, name, middle_name, date_of_birth, passport_data, residence_address, phone)
VALUES ('ivanov', 'ivan', 'ivanovich', '1978-10-06 10:56:16.310914', '3123452 41534154',
        'Vologda,prospect mira 32a street,32 apt', '88005553555');
INSERT INTO contract (human_id, flat_id, date_contract, surname_employee, downpayment)
VALUES (1, 56, '2020-06-06 14:12:16.310914', 'Garshin', 453642.23);

SELECT COUNT(number_flat)
FROM flat AS f
WHERE NOT EXISTS(SELECT * FROM contract AS c WHERE c.flat_id = f.id)
  and construction_id = 1;


SELECT human.surname,
       human.name,
       human.middle_name,
       construction.heating,
       construction.gas,
       construction.date_fundament,
       construction_position.address
FROM human
         JOIN Construction ON Construction.id = (SELECT construction_id
                                                 FROM flat AS f
                                                 WHERE f.id = (SELECT flat_id FROM contract WHERE human_id = human.id))
         JOIN construction_position ON construction_position.id = construction.id;
