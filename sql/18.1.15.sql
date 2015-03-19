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
47	Longitude	43.2	\N	\N	46
48	Latitude	42.3	\N	\N	46
79	Location	\N	63	2	\N
80	Latitude	42.3	\N	\N	79
81	Longitude	43.2	\N	\N	79
84	Location	\N	63	3	\N
85	Latitude	42.3	\N	\N	84
86	Longitude	43.2	\N	\N	84
46	Location	\N	63	1	\N
\.


--
-- Name: contexts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: linkeex
--

SELECT pg_catalog.setval('contexts_id_seq', 86, true);


--
-- Data for Name: persons; Type: TABLE DATA; Schema: public; Owner: linkeex
--

COPY persons (id, name, "timestamp") FROM stdin;
143	Alice	1
63	Tim	2
145	Alice	1
63	Tim	3
63	Tim	1
\.


--
-- Name: persons_id_seq; Type: SEQUENCE SET; Schema: public; Owner: linkeex
--

SELECT pg_catalog.setval('persons_id_seq', 145, true);


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

