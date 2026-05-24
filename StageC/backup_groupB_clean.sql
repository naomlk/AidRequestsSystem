--
-- PostgreSQL database dump
--

-- backupo edit
-- changer le nom de la containte de la cle primaire de volunteer ar cets la meme ds les 2 tabes
-- ch,ager le nom de auteur en ochrith


\restrict kFtzmYXleuzGCEiQVfOehfGn3Hi7Kc6kQaThjkKewnjgPM4NWqoFTPLxf7myKiP

-- Dumped from database version 18.3 (Debian 18.3-1.pgdg13+1)
-- Dumped by pg_dump version 18.3

-- Started on 2026-05-12 08:28:39 UTC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

-- CREATE SCHEMA public;


-- ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- TOC entry 3561 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 219 (class 1259 OID 24577)
-- Name: availability; Type: TABLE; Schema: public; Owner: ochrith
--

CREATE TABLE public.b_availability (
    day_of_week character varying(10) NOT NULL,
    start_time character varying(5) NOT NULL,
    end_time character varying(5) NOT NULL,
    preferred_region_ character varying(20) NOT NULL,
    volunteer_id integer NOT NULL,
    CONSTRAINT availability_check CHECK (((start_time)::text < (end_time)::text)),
    CONSTRAINT availability_day_of_week_check CHECK (((day_of_week)::text = ANY (ARRAY[('Sunday'::character varying)::text, ('Monday'::character varying)::text, ('Tuesday'::character varying)::text, ('Wednesday'::character varying)::text, ('Thursday'::character varying)::text, ('Friday'::character varying)::text, ('Saturday'::character varying)::text])))
);


ALTER TABLE public.b_availability OWNER TO "ochrith";

--
-- TOC entry 220 (class 1259 OID 24587)
-- Name: call; Type: TABLE; Schema: public; Owner: ochrith
--

CREATE TABLE public.b_call (
    longitude double precision NOT NULL,
    call_time time without time zone NOT NULL,
    status character varying(15) NOT NULL,
    call_id integer NOT NULL,
    phone integer NOT NULL,
    call_date date NOT NULL,
    latitude integer NOT NULL,
    description text,
    type_id integer NOT NULL,
    CONSTRAINT call_status_check CHECK (((status)::text = ANY (ARRAY[('Open'::character varying)::text, ('Closed'::character varying)::text, ('InProgress'::character varying)::text]))),
    CONSTRAINT check_call_time_not_null CHECK ((call_time IS NOT NULL))
);


ALTER TABLE public.b_call OWNER TO "ochriht";

--
-- TOC entry 221 (class 1259 OID 24601)
-- Name: catagory; Type: TABLE; Schema: public; Owner: ochrith
--

CREATE TABLE public.b_catagory (
    catagory_id integer NOT NULL,
    catagory_name character varying(20) NOT NULL,
    CONSTRAINT catagory_catagory_name_check CHECK (((catagory_name)::text = ANY (ARRAY[('Language'::character varying)::text, ('Vehicle'::character varying)::text, ('Locksmith'::character varying)::text, ('Rescue'::character varying)::text, ('Technical'::character varying)::text, ('Emergency'::character varying)::text])))
);


ALTER TABLE public.b_catagory OWNER TO "ochrith";

--
-- TOC entry 222 (class 1259 OID 24607)
-- Name: scheduled; Type: TABLE; Schema: public; Owner: ochrith
--

CREATE TABLE public.b_scheduled (
    meeting_date date NOT NULL,
    start_time character varying(5) NOT NULL,
    location character varying(20) NOT NULL,
    end_time character varying(5) NOT NULL,
    training_id integer NOT NULL,
    CONSTRAINT scheduled_check CHECK (((start_time)::text < (end_time)::text))
);


ALTER TABLE public.b_scheduled OWNER TO "ochrith";

--
-- TOC entry 223 (class 1259 OID 24616)
-- Name: skill; Type: TABLE; Schema: public; Owner: ochrith
--

CREATE TABLE public.b_skill (
    skill_id integer NOT NULL,
    description text,
    requires_certificate character(1) NOT NULL,
    difficulty_level integer NOT NULL,
    skill_name character varying(15) NOT NULL,
    CONSTRAINT skill_difficulty_level_check CHECK (((difficulty_level >= 1) AND (difficulty_level <= 5))),
    CONSTRAINT skill_requires_certificate_check CHECK ((requires_certificate = ANY (ARRAY['Y'::bpchar, 'N'::bpchar])))
);


ALTER TABLE public.b_skill OWNER TO "ochrith";

--
-- TOC entry 224 (class 1259 OID 24627)
-- Name: skill_category; Type: TABLE; Schema: public; Owner: ochrith
--

CREATE TABLE public.b_skill_category (
    skill_id integer NOT NULL,
    catagory_id integer NOT NULL
);


ALTER TABLE public.b_skill_category OWNER TO "ochrith";

--
-- TOC entry 225 (class 1259 OID 24632)
-- Name: training; Type: TABLE; Schema: public; Owner: ochrith
--

CREATE TABLE public.b_training (
    training_name character varying(15) NOT NULL,
    description_ character varying(30) NOT NULL,
    max_participant integer NOT NULL,
    duration_hours integer NOT NULL,
    training_id integer NOT NULL,
    CONSTRAINT check_training_duration CHECK ((duration_hours <= 10)),
    CONSTRAINT training_duration_hours_check CHECK ((duration_hours > 0)),
    CONSTRAINT training_max_participant_check CHECK ((max_participant > 0))
);


ALTER TABLE public.b_training OWNER TO "ochrith";

--
-- TOC entry 226 (class 1259 OID 24642)
-- Name: type; Type: TABLE; Schema: public; Owner: ochrith
--

CREATE TABLE public.b_type (
    type_id integer NOT NULL,
    type_name character varying(40) NOT NULL,
    CONSTRAINT type_type_name_check CHECK (((type_name)::text = ANY (ARRAY[('Flat Tire Assistance'::character varying)::text, ('Locked Vehicle'::character varying)::text, ('Stuck In Elevator'::character varying)::text, ('Child Locked In Car'::character varying)::text, ('Locked Home Door'::character varying)::text, ('Search And Rescue'::character varying)::text])))
);


ALTER TABLE public.b_type OWNER TO "ochrith";

--
-- TOC entry 227 (class 1259 OID 24648)
-- Name: volunteer; Type: TABLE; Schema: public; Owner: ochrith
--

CREATE TABLE public.b_volunteer (
    first_name character varying(20) NOT NULL,
    phone integer NOT NULL,
    birthday date NOT NULL,
    email text NOT NULL,
    city character varying(30) NOT NULL,
    volunteer_id integer NOT NULL,
    recruitment_date date NOT NULL,
    last_name character varying(20) NOT NULL,
    is_active character(1) NOT NULL,
    CONSTRAINT check_phone_positive CHECK ((phone > 0)),
    CONSTRAINT volunteer_birthday_check CHECK ((birthday < CURRENT_DATE)),
    CONSTRAINT volunteer_check CHECK ((recruitment_date >= birthday)),
    CONSTRAINT volunteer_is_active_check CHECK ((is_active = ANY (ARRAY['Y'::bpchar, 'N'::bpchar]))),
    CONSTRAINT volunteer_recruitment_date_check CHECK ((recruitment_date <= CURRENT_DATE))
);


ALTER TABLE public.b_volunteer OWNER TO "ochrith";

--
-- TOC entry 228 (class 1259 OID 24666)
-- Name: volunteer_call; Type: TABLE; Schema: public; Owner: ochrith
--

CREATE TABLE public.b_volunteer_call (
    volunteer_id integer NOT NULL,
    call_id integer NOT NULL
);


ALTER TABLE public.b_volunteer_call OWNER TO "ochrith";

--
-- TOC entry 229 (class 1259 OID 24671)
-- Name: volunteer_skill; Type: TABLE; Schema: public; Owner: ochrith
--

CREATE TABLE public.b_volunteer_skill (
    volunteer_id integer NOT NULL,
    skill_id integer NOT NULL
);


ALTER TABLE public.b_volunteer_skill OWNER TO "ochrith";

--
-- TOC entry 230 (class 1259 OID 24676)
-- Name: volunteer_training; Type: TABLE; Schema: public; Owner: ochrith
--

CREATE TABLE public.b_volunteer_training (
    training_id integer NOT NULL,
    volunteer_id integer NOT NULL
);


ALTER TABLE public.b_volunteer_training OWNER TO "ochrith";

--
-- TOC entry 3544 (class 0 OID 24577)
-- Dependencies: 219
-- Data for Name: availability; Type: TABLE DATA; Schema: public; Owner: ochrith
--

COPY public.b_availability (day_of_week, start_time, end_time, preferred_region_, volunteer_id) FROM stdin;
\.


--
-- TOC entry 3545 (class 0 OID 24587)
-- Dependencies: 220
-- Data for Name: call; Type: TABLE DATA; Schema: public; Owner: ochrith
--

COPY public.b_call (longitude, call_time, status, call_id, phone, call_date, latitude, description, type_id) FROM stdin;
35.21	11:40:00	Closed	2	509222222	2026-04-10	31	Car locked	2
34.75	13:05:00	Closed	4	509444444	2026-04-11	32	Child locked	4
35.01	19:30:00	Open	5	509555555	2026-04-12	31	Door locked	5
34.8	14:20:00	Open	6	508666666	2026-04-13	32	Flat tire	1
35.1	17:45:00	Closed	7	508777777	2026-04-14	31	Car locked	2
34.7	20:00:00	Open	9	508999999	2026-04-16	32	Child locked	4
35	12:30:00	Closed	10	509000000	2026-04-17	31	Door locked	5
34.88	10:10:00	Open	11	507111111	2026-04-18	32	Flat tire	1
35.12	11:20:00	Closed	12	507222222	2026-04-18	31	Car locked	2
34.72	18:00:00	Closed	14	507444444	2026-04-19	32	Child locked	4
35.02	13:00:00	Open	15	507555555	2026-04-20	31	Door locked	5
34.81	09:25:00	Open	16	507666666	2026-04-21	32	Flat tire	1
35.14	10:40:00	Closed	17	507777777	2026-04-21	31	Car locked	2
34.74	14:15:00	Open	19	507999999	2026-04-22	32	Child locked	4
35.03	16:20:00	Closed	20	508000000	2026-04-23	31	Door locked	5
34.99	08:20:00	InProgress	3	509333333	2026-04-11	32	URGENT: Long duration in progress - Elevator stuck	3
34.9	09:10:00	InProgress	8	508888888	2026-04-15	32	URGENT: Long duration in progress - Elevator stuck	3
34.95	09:30:00	InProgress	13	507333333	2026-04-19	32	URGENT: Long duration in progress - Elevator stuck	3
34.97	12:05:00	InProgress	18	507888888	2026-04-22	32	URGENT: Long duration in progress - Elevator stuck	3
34.78	10:15:00	Closed	1	509111111	2026-04-10	32	Flat tire	1
\.


--
-- TOC entry 3546 (class 0 OID 24601)
-- Dependencies: 221
-- Data for Name: catagory; Type: TABLE DATA; Schema: public; Owner: ochrith
--

COPY public.b_catagory (catagory_id, catagory_name) FROM stdin;
1	Language
2	Vehicle
3	Locksmith
4	Rescue
5	Technical
6	Emergency
\.


--
-- TOC entry 3547 (class 0 OID 24607)
-- Dependencies: 222
-- Data for Name: scheduled; Type: TABLE DATA; Schema: public; Owner: ochrith
--

COPY public.b_scheduled (meeting_date, start_time, location, end_time, training_id) FROM stdin;
\.


--
-- TOC entry 3548 (class 0 OID 24616)
-- Dependencies: 223
-- Data for Name: skill; Type: TABLE DATA; Schema: public; Owner: ochrith
--

COPY public.b_skill (skill_id, description, requires_certificate, difficulty_level, skill_name) FROM stdin;
1	English speaking	N	1	English
2	French speaking	N	2	French
3	Tire replacement	N	3	Tire
4	Car unlocking	N	4	Unlock
6	Hebrew speaking	N	1	Hebrew
7	Arabic speaking	N	2	Arabic
8	Basic mechanics	N	3	Mechanics
9	Radio communication	N	2	Radio
11	Navigation	N	2	Navigation
12	Technical repair	N	3	Technical
14	Vehicle support	N	2	Vehicle
15	Locksmith skills	N	4	Locksmith
5	Elevator rescue	Y	5	Elevator
10	First aid	Y	5	FirstAid
13	Emergency response	Y	5	Emergency
\.


--
-- TOC entry 3549 (class 0 OID 24627)
-- Dependencies: 224
-- Data for Name: skill_category; Type: TABLE DATA; Schema: public; Owner: ochrith
--

COPY public.b_skill_category (skill_id, catagory_id) FROM stdin;
\.


--
-- TOC entry 3550 (class 0 OID 24632)
-- Dependencies: 225
-- Data for Name: training; Type: TABLE DATA; Schema: public; Owner: ochrith
--

COPY public.b_training (training_name, description_, max_participant, duration_hours, training_id) FROM stdin;
Medic	First aid	20	4	7
BasicAid	Intro help	25	5	1
SearchUnit	Search training	30	7	5
RoadHelp	Road assist	22	4	6
RadioUse	Radio training	28	3	13
Emergency1	Emergency	26	6	14
Locks	Vehicle lock	25	3	2
Elevators	Elevator rescue	20	5	3
ChildRescue	Child safety	23	4	4
CarAccess	Vehicle access	23	3	8
HomeEntry	Door opening	20	2	9
LiftSafe	Lift safety	17	5	10
RescuePro	Rescue pro	25	6	11
FieldTech	Tech work	24	4	12
Navigation	Navigation	23	3	15
\.


--
-- TOC entry 3551 (class 0 OID 24642)
-- Dependencies: 226
-- Data for Name: type; Type: TABLE DATA; Schema: public; Owner: ochrith
--

COPY public.b_type (type_id, type_name) FROM stdin;
1	Flat Tire Assistance
2	Locked Vehicle
3	Stuck In Elevator
4	Child Locked In Car
5	Locked Home Door
6	Search And Rescue
\.


--
-- TOC entry 3552 (class 0 OID 24648)
-- Dependencies: 227
-- Data for Name: volunteer; Type: TABLE DATA; Schema: public; Owner: ochrith
--

COPY public.b_volunteer (first_name, phone, birthday, email, city, volunteer_id, recruitment_date, last_name, is_active) FROM stdin;
Dana	503333333	1999-02-14	dana@gmail.com	Jerusalem	3	2023-03-10	Mizrahi	Y
Eitan	504444444	1992-07-30	eitan@gmail.com	Ashdod	4	2020-04-05	Biton	N
Omer	509444444	1994-09-17	omer@gmail.com	Ashkelon	9	2022-06-10	Bar	N
Ron	504333000	1993-01-10	ron@gmail.com	Jerusalem	13	2020-09-09	Tal	N
Neta	508777000	1997-06-18	neta@gmail.com	Haifa	17	2022-04-12	Rosen	Y
Gal	509888000	1994-11-05	gal@gmail.com	Jerusalem	18	2021-07-20	BenAmi	N
Amit	506111111	1996-03-11	amit@gmail.com	TelAviv	6	2021-05-05	David	Y
Adi	503222000	1996-07-07	adi@gmail.com	TelAviv	12	2021-03-15	Haim	Y
Eli	507666000	1992-02-02	eli@gmail.com	TelAviv	16	2020-02-02	Mor	Y
Yuval	502888111	1993-09-09	yuval@gmail.com	TelAviv	20	2020-11-11	Golan	Y
Shira	505555555	1997-12-09	shira@gmail.com	Netanya	5	2022-09-20	Avraham	N
Lior	507222222	1993-11-02	lior@gmail.com	Haifa	7	2020-08-12	Katz	N
Rina	508333333	2000-01-25	rina@gmail.com	Jerusalem	8	2023-01-01	Peretz	N
Maya	505444000	1999-11-11	maya@gmail.com	Ashdod	14	2023-01-20	Barak	N
Dean	501999000	1998-08-22	dean@gmail.com	Netanya	19	2022-10-01	Yosef	N
Tamar	501000000	1998-12-30	tamar@gmail.com	Netanya	10	2023-02-02	Nissan	N
Gil	502111000	1997-04-04	gil@gmail.com	Haifa	11	2022-05-01	Shalom	N
Idan	506555000	1995-06-06	idan@gmail.com	Netanya	15	2022-08-08	Or	N
Noa	501111111	1998-05-10	noa@gmail.com	TelAviv	1	2022-01-01	Levi	N
Yossi	502222222	1995-08-21	yossi@gmail.com	Tel Aviv	2	2021-06-15	Cohen	N
\.


--
-- TOC entry 3553 (class 0 OID 24666)
-- Dependencies: 228
-- Data for Name: volunteer_call; Type: TABLE DATA; Schema: public; Owner: ochrith
--

COPY public.b_volunteer_call (volunteer_id, call_id) FROM stdin;
3	3
6	6
12	12
12	20
12	1
17	9
3	7
12	2
20	11
17	20
16	7
17	14
17	18
20	20
6	5
3	10
17	8
12	15
12	7
16	15
6	4
20	17
3	20
6	2
16	4
6	12
6	17
16	19
3	4
6	18
6	20
3	1
3	15
16	18
16	14
3	12
3	8
6	3
16	10
20	5
20	13
6	10
20	19
20	18
17	4
12	11
3	19
17	2
6	1
3	13
20	14
20	1
3	17
16	1
6	8
16	5
3	2
16	20
20	8
17	3
16	11
12	3
20	3
17	10
12	17
12	8
16	8
17	13
20	9
3	16
6	16
16	6
12	18
12	19
6	14
20	16
16	16
20	10
16	17
20	12
12	6
17	5
17	1
17	11
12	10
3	6
20	6
16	9
12	4
17	19
17	15
12	16
6	9
20	4
6	11
17	17
20	2
16	12
16	3
3	5
12	14
16	2
16	13
17	6
3	18
6	19
6	15
12	5
3	14
17	7
6	13
17	12
12	9
20	15
17	16
3	11
\.


--
-- TOC entry 3554 (class 0 OID 24671)
-- Dependencies: 229
-- Data for Name: volunteer_skill; Type: TABLE DATA; Schema: public; Owner: ochrith
--

COPY public.b_volunteer_skill (volunteer_id, skill_id) FROM stdin;
3	5
6	6
12	12
16	1
17	2
3	13
3	1
16	13
6	12
3	3
16	8
3	9
3	10
12	3
12	2
6	4
3	8
17	5
16	9
17	13
6	11
17	11
17	3
20	9
16	2
3	7
12	6
6	14
6	10
6	1
6	15
12	10
20	2
20	5
20	10
20	12
16	15
20	4
12	1
16	7
16	10
20	6
16	14
17	6
12	15
20	3
6	7
17	10
12	11
17	8
17	9
12	9
3	12
6	3
20	11
16	3
16	5
17	12
3	14
6	9
17	4
20	15
17	15
20	14
6	13
6	5
12	13
16	12
3	6
17	14
17	1
12	5
12	4
12	8
20	7
16	11
12	14
20	8
20	1
3	11
16	4
3	2
3	4
6	2
12	7
20	13
17	7
3	15
\.


--
-- TOC entry 3555 (class 0 OID 24676)
-- Dependencies: 230
-- Data for Name: volunteer_training; Type: TABLE DATA; Schema: public; Owner: ochrith
--

COPY public.b_volunteer_training (training_id, volunteer_id) FROM stdin;
3	3
4	3
6	6
7	6
11	20
10	17
12	16
2	12
1	16
11	6
9	12
3	12
5	16
1	6
14	6
6	3
13	16
12	3
7	17
13	12
5	20
2	17
11	17
1	17
12	17
3	20
3	17
15	16
12	6
1	20
10	20
11	3
9	16
15	3
5	6
5	17
6	20
14	17
7	20
15	12
11	12
6	12
5	12
15	20
5	3
7	16
4	17
14	3
1	3
13	6
10	12
10	6
6	17
8	12
9	20
8	20
2	16
14	16
14	12
12	20
3	6
15	6
4	16
10	16
4	20
3	16
8	3
7	3
9	6
9	3
13	20
6	16
7	12
13	17
12	12
13	3
8	6
8	17
1	12
4	12
2	3
9	17
2	20
14	20
2	6
4	6
11	16
\.


--
-- TOC entry 3350 (class 2606 OID 24682)
-- Name: availability availability_pkey; Type: CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_availability
    ADD CONSTRAINT availability_pkey PRIMARY KEY (day_of_week, start_time, volunteer_id);


--
-- TOC entry 3352 (class 2606 OID 24684)
-- Name: call call_pkey; Type: CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_call
    ADD CONSTRAINT call_pkey PRIMARY KEY (call_id);


--
-- TOC entry 3355 (class 2606 OID 24686)
-- Name: catagory catagory_catagory_name_key; Type: CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_catagory
    ADD CONSTRAINT catagory_catagory_name_key UNIQUE (catagory_name);


--
-- TOC entry 3357 (class 2606 OID 24688)
-- Name: catagory catagory_pkey; Type: CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_catagory
    ADD CONSTRAINT catagory_pkey PRIMARY KEY (catagory_id);


--
-- TOC entry 3359 (class 2606 OID 24690)
-- Name: scheduled scheduled_pkey; Type: CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_scheduled
    ADD CONSTRAINT scheduled_pkey PRIMARY KEY (training_id, meeting_date, start_time);


--
-- TOC entry 3365 (class 2606 OID 24692)
-- Name: skill_category skill_category_pkey; Type: CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_skill_category
    ADD CONSTRAINT skill_category_pkey PRIMARY KEY (skill_id, catagory_id);


--
-- TOC entry 3361 (class 2606 OID 24694)
-- Name: skill skill_pkey; Type: CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_skill
    ADD CONSTRAINT skill_pkey PRIMARY KEY (skill_id);


--
-- TOC entry 3363 (class 2606 OID 24696)
-- Name: skill skill_skill_name_key; Type: CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_skill
    ADD CONSTRAINT skill_skill_name_key UNIQUE (skill_name);


--
-- TOC entry 3367 (class 2606 OID 24698)
-- Name: training training_pkey; Type: CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_training
    ADD CONSTRAINT training_pkey PRIMARY KEY (training_id);


--
-- TOC entry 3369 (class 2606 OID 24700)
-- Name: type type_pkey; Type: CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_type
    ADD CONSTRAINT type_pkey PRIMARY KEY (type_id);


--
-- TOC entry 3371 (class 2606 OID 24702)
-- Name: type type_type_name_key; Type: CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_type
    ADD CONSTRAINT type_type_name_key UNIQUE (type_name);


--
-- TOC entry 3381 (class 2606 OID 24704)
-- Name: volunteer_call volunteer_call_pkey; Type: CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_volunteer_call
    ADD CONSTRAINT volunteer_call_pkey PRIMARY KEY (volunteer_id, call_id);


--
-- TOC entry 3374 (class 2606 OID 24706)
-- Name: volunteer volunteer_email_key; Type: CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_volunteer
    ADD CONSTRAINT volunteer_email_key UNIQUE (email);


--
-- TOC entry 3376 (class 2606 OID 24708)
-- Name: volunteer volunteer_phone_key; Type: CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_volunteer
    ADD CONSTRAINT volunteer_phone_key UNIQUE (phone);


--
-- TOC entry 3378 (class 2606 OID 24710)
-- Name: volunteer volunteer_pkey; Type: CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_volunteer
    ADD CONSTRAINT b_volunteer_pkey PRIMARY KEY (volunteer_id);




--
-- TOC entry 3383 (class 2606 OID 24712)
-- Name: volunteer_skill volunteer_skill_pkey; Type: CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_volunteer_skill
    ADD CONSTRAINT volunteer_skill_pkey PRIMARY KEY (volunteer_id, skill_id);


--
-- TOC entry 3385 (class 2606 OID 24714)
-- Name: volunteer_training volunteer_training_pkey; Type: CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_volunteer_training
    ADD CONSTRAINT volunteer_training_pkey PRIMARY KEY (training_id, volunteer_id);


--
-- TOC entry 3353 (class 1259 OID 32775)
-- Name: idx_call_type_id; Type: INDEX; Schema: public; Owner: ochrith
--

CREATE INDEX idx_call_type_id ON public.b_call USING btree (type_id);


--
-- TOC entry 3379 (class 1259 OID 32774)
-- Name: idx_volunteer_call_volunteer_id; Type: INDEX; Schema: public; Owner: ochrith
--

CREATE INDEX idx_volunteer_call_volunteer_id ON public.b_volunteer_call USING btree (volunteer_id);


--
-- TOC entry 3372 (class 1259 OID 32776)
-- Name: idx_volunteer_is_active; Type: INDEX; Schema: public; Owner: ochrith
--

CREATE INDEX idx_volunteer_is_active ON public.b_volunteer USING btree (is_active);


--
-- TOC entry 3386 (class 2606 OID 24715)
-- Name: availability availability_volunteer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_availability
    ADD CONSTRAINT availability_volunteer_id_fkey FOREIGN KEY (volunteer_id) REFERENCES public.b_volunteer(volunteer_id);


--
-- TOC entry 3387 (class 2606 OID 24720)
-- Name: call call_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_call
    ADD CONSTRAINT call_type_id_fkey FOREIGN KEY (type_id) REFERENCES public.b_type(type_id);


--
-- TOC entry 3388 (class 2606 OID 24725)
-- Name: scheduled scheduled_training_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_scheduled
    ADD CONSTRAINT scheduled_training_id_fkey FOREIGN KEY (training_id) REFERENCES public.b_training(training_id);


--
-- TOC entry 3389 (class 2606 OID 24730)
-- Name: skill_category skill_category_catagory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_skill_category
    ADD CONSTRAINT skill_category_catagory_id_fkey FOREIGN KEY (catagory_id) REFERENCES public.b_catagory(catagory_id);


--
-- TOC entry 3390 (class 2606 OID 24735)
-- Name: skill_category skill_category_skill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_skill_category
    ADD CONSTRAINT skill_category_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES public.b_skill(skill_id);


--
-- TOC entry 3391 (class 2606 OID 24740)
-- Name: volunteer_call volunteer_call_call_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_volunteer_call
    ADD CONSTRAINT volunteer_call_call_id_fkey FOREIGN KEY (call_id) REFERENCES public.b_call(call_id);


--
-- TOC entry 3392 (class 2606 OID 24745)
-- Name: volunteer_call volunteer_call_volunteer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_volunteer_call
    ADD CONSTRAINT volunteer_call_volunteer_id_fkey FOREIGN KEY (volunteer_id) REFERENCES public.b_volunteer(volunteer_id);


--
-- TOC entry 3393 (class 2606 OID 24750)
-- Name: volunteer_skill volunteer_skill_skill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_volunteer_skill
    ADD CONSTRAINT volunteer_skill_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES public.b_skill(skill_id);


--
-- TOC entry 3394 (class 2606 OID 24755)
-- Name: volunteer_skill volunteer_skill_volunteer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_volunteer_skill
    ADD CONSTRAINT volunteer_skill_volunteer_id_fkey FOREIGN KEY (volunteer_id) REFERENCES public.b_volunteer(volunteer_id);


--
-- TOC entry 3395 (class 2606 OID 24760)
-- Name: volunteer_training volunteer_training_training_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_volunteer_training
    ADD CONSTRAINT volunteer_training_training_id_fkey FOREIGN KEY (training_id) REFERENCES public.b_training(training_id);


--
-- TOC entry 3396 (class 2606 OID 24765)
-- Name: volunteer_training volunteer_training_volunteer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ochrith
--

ALTER TABLE ONLY public.b_volunteer_training
    ADD CONSTRAINT volunteer_training_volunteer_id_fkey FOREIGN KEY (volunteer_id) REFERENCES public.b_volunteer(volunteer_id);


-- Completed on 2026-05-12 08:28:39 UTC

--
-- PostgreSQL database dump complete
--

\unrestrict kFtzmYXleuzGCEiQVfOehfGn3Hi7Kc6kQaThjkKewnjgPM4NWqoFTPLxf7myKiP

