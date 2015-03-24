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

--
-- Name: update_modified_column(); Type: FUNCTION; Schema: public; Owner: linkeex
--

CREATE FUNCTION update_modified_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.modified = now();
    RETURN NEW;	
END;
$$;


ALTER FUNCTION public.update_modified_column() OWNER TO linkeex;

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
    modified timestamp without time zone,
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
    "timestamp" integer NOT NULL,
    modified timestamp without time zone
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

COPY contexts (id, key, value, personid, persontimestamp, contextid, modified) FROM stdin;
157	Polygon	\N	63	2	\N	2015-03-19 23:34:38.468678
158	Location	\N	\N	\N	157	2015-03-19 23:34:38.470397
159	Latitude	42.3	\N	\N	158	2015-03-19 23:34:38.471107
160	Longitude	43.2	\N	\N	158	2015-03-19 23:34:38.47169
2	Longitude	43.2	\N	\N	1	2015-03-19 22:51:54.908657
3	Latitude	42.3	\N	\N	1	2015-03-19 22:52:06.274008
4	Polygon	\N	63	1	\N	2015-03-19 23:31:12.171092
1	Location	\N	\N	\N	4	2015-03-19 22:51:37.039527
\.


--
-- Name: contexts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: linkeex
--

SELECT pg_catalog.setval('contexts_id_seq', 160, true);


--
-- Data for Name: persons; Type: TABLE DATA; Schema: public; Owner: linkeex
--

COPY persons (id, name, "timestamp", modified) FROM stdin;
63	Tim	1	2015-03-19 22:51:15.666199
191	Alice	1	2015-03-19 23:34:38.461672
63	Tim	2	2015-03-19 23:34:38.468678
\.


--
-- Name: persons_id_seq; Type: SEQUENCE SET; Schema: public; Owner: linkeex
--

SELECT pg_catalog.setval('persons_id_seq', 191, true);


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
-- Name: update_context_modtime; Type: TRIGGER; Schema: public; Owner: linkeex
--

CREATE TRIGGER update_context_modtime BEFORE INSERT ON contexts FOR EACH ROW EXECUTE PROCEDURE update_modified_column();


--
-- Name: update_person_modtime; Type: TRIGGER; Schema: public; Owner: linkeex
--

CREATE TRIGGER update_person_modtime BEFORE INSERT ON persons FOR EACH ROW EXECUTE PROCEDURE update_modified_column();


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

