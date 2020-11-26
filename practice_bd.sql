CREATE TABLE User_Site(
    Id SERIAL PRIMARY KEY,
    email CHARACTER VARYING(255),
    password_hash CHARACTER VARYING(255),
    isUser bool default true,
    isAdmin bool default false
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


