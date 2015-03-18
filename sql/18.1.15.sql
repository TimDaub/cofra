--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: contexts; Type: TABLE; Schema: public; Owner: linkeex; Tablespace: 
--

CREATE TABLE contexts (
    id integer NOT NULL,
    key text NOT NULL,
    value text,
    personid integer,
    persontimestamp integer,
    contextid integer,
    CONSTRAINT valid_parent CHECK (((((contextid IS NOT NULL) AND (personid IS NULL)) AND (persontimestamp IS NULL)) OR (((contextid IS NULL) AND (personid IS NOT NULL)) AND (persontimestamp IS NOT NULL))))
);


ALTER TABLE public.contexts OWNER TO linkeex;

--
-- Name: contexts_id_seq; Type: SEQUENCE; Schema: public; Owner: linkeex
--

CREATE SEQUENCE contexts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.contexts_id_seq OWNER TO linkeex;

--
-- Name: contexts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: linkeex
--

ALTER SEQUENCE contexts_id_seq OWNED BY contexts.id;


--
-- Name: persons; Type: TABLE; Schema: public; Owner: linkeex; Tablespace: 
--

CREATE TABLE persons (
    id integer NOT NULL,
    name text NOT NULL,
    "timestamp" integer NOT NULL
);


ALTER TABLE public.persons OWNER TO linkeex;

--
-- Name: persons_id_seq; Type: SEQUENCE; Schema: public; Owner: linkeex
--

CREATE SEQUENCE persons_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.persons_id_seq OWNER TO linkeex;

--
-- Name: persons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: linkeex
--

ALTER SEQUENCE persons_id_seq OWNED BY persons.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: linkeex
--

ALTER TABLE ONLY contexts ALTER COLUMN id SET DEFAULT nextval('contexts_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: linkeex
--

ALTER TABLE ONLY persons ALTER COLUMN id SET DEFAULT nextval('persons_id_seq'::regclass);


--
-- Data for Name: contexts; Type: TABLE DATA; Schema: public; Owner: linkeex
--

COPY contexts (id, key, value, personid, persontimestamp, contextid) FROM stdin;
1	Polygon	\N	63	1	\N
2	Location	\N	\N	\N	1
3	Longitude	43.2	\N	\N	2
4	Latitude	42.3	\N	\N	2
5	Temperature	23	73	1	\N
6	Temperature	23	73	1	\N
7	Temperature	23	75	1	\N
8	Temperature	23	75	1	\N
9	Temperature	23	77	1	\N
10	Temperature	23	77	1	\N
11	Temperature	23	79	1	\N
12	Temperature	23	79	1	\N
13	Temperature	23	81	1	\N
14	Temperature	23	81	1	\N
15	Temperature	23	83	1	\N
16	Temperature	23	83	1	\N
17	Temperature	23	85	1	\N
18	Temperature	23	85	1	\N
19	Temperature	23	87	1	\N
20	Temperature	23	87	1	\N
21	Temperature	23	89	1	\N
22	Temperature	23	89	1	\N
\.


--
-- Name: contexts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: linkeex
--

SELECT pg_catalog.setval('contexts_id_seq', 22, true);


--
-- Data for Name: persons; Type: TABLE DATA; Schema: public; Owner: linkeex
--

COPY persons (id, name, "timestamp") FROM stdin;
77	Alice	0
77	Alice	1
79	Alice	0
79	Alice	1
81	Alice	0
81	Alice	1
83	Alice	0
83	Alice	1
85	Alice	0
63	Alice	1
85	Alice	1
87	Alice	0
87	Alice	1
64	Bob	1
89	Alice	0
65	Alice	0
65	Alice	1
89	Alice	1
67	Alice	0
67	Alice	1
69	Alice	0
69	Alice	1
71	Alice	0
71	Alice	1
73	Alice	0
73	Alice	1
75	Alice	0
75	Alice	1
\.


--
-- Name: persons_id_seq; Type: SEQUENCE SET; Schema: public; Owner: linkeex
--

SELECT pg_catalog.setval('persons_id_seq', 89, true);


--
-- Name: contexts_pkey; Type: CONSTRAINT; Schema: public; Owner: linkeex; Tablespace: 
--

ALTER TABLE ONLY contexts
    ADD CONSTRAINT contexts_pkey PRIMARY KEY (id);


--
-- Name: persons_pkey; Type: CONSTRAINT; Schema: public; Owner: linkeex; Tablespace: 
--

ALTER TABLE ONLY persons
    ADD CONSTRAINT persons_pkey PRIMARY KEY (id, "timestamp");


--
-- Name: contexts_contextid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: linkeex
--

ALTER TABLE ONLY contexts
    ADD CONSTRAINT contexts_contextid_fkey FOREIGN KEY (contextid) REFERENCES contexts(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: contexts_personid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: linkeex
--

ALTER TABLE ONLY contexts
    ADD CONSTRAINT contexts_personid_fkey FOREIGN KEY (personid, persontimestamp) REFERENCES persons(id, "timestamp") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: public; Type: ACL; Schema: -; Owner: linkeex
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM linkeex;
GRANT ALL ON SCHEMA public TO linkeex;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

