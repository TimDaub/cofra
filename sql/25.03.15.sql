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
388	Longitude	43.2	63	2	\N	2015-03-24 23:24:13.684376
391	Longitude	43.2	63	4	\N	2015-03-24 23:51:35.669839
392	Somethingelse	42.3	\N	\N	391	2015-03-24 23:51:35.679112
393	Latitude	42.3	63	4	\N	2015-03-24 23:51:35.680078
398	Longitude	43.2	63	6	\N	2015-03-24 23:52:26.979177
399	Somethingelse	42.3	\N	\N	398	2015-03-24 23:52:26.985695
400	jndkjasndaksjnd	42.3	\N	\N	399	2015-03-24 23:52:26.986658
401	Latitude	42.3	63	6	\N	2015-03-24 23:52:26.98751
402	voooolllcoool	42.3	\N	\N	401	2015-03-24 23:52:26.988436
409	Longitude	43.2	63	8	\N	2015-03-25 00:12:59.837717
410	Somethingelse	42.3	\N	\N	409	2015-03-25 00:12:59.845712
411	Latitude	42.3	63	8	\N	2015-03-25 00:12:59.846664
412	voooolllcoool	42.3	\N	\N	411	2015-03-25 00:12:59.847683
413	uncool	42.3	63	8	\N	2015-03-25 00:12:59.8486
418	Longitude	43.2	63	10	\N	2015-03-25 00:13:26.022779
419	Latitude	42.3	63	10	\N	2015-03-25 00:13:26.029265
420	uncool	42.3	63	10	\N	2015-03-25 00:13:26.030882
423	uncool	42.3	63	12	\N	2015-03-25 00:13:46.125429
389	Longitude	43.2	63	3	\N	2015-03-24 23:24:29.14698
390	Latitude	42.3	63	3	\N	2015-03-24 23:24:29.153129
394	Longitude	43.2	63	5	\N	2015-03-24 23:52:12.738128
395	Somethingelse	42.3	\N	\N	394	2015-03-24 23:52:12.744633
396	jndkjasndaksjnd	42.3	\N	\N	395	2015-03-24 23:52:12.745415
397	Latitude	42.3	63	5	\N	2015-03-24 23:52:12.746104
403	Longitude	43.2	63	7	\N	2015-03-24 23:52:40.658517
404	Somethingelse	42.3	\N	\N	403	2015-03-24 23:52:40.664849
405	jndkjasndaksjnd	42.3	\N	\N	404	2015-03-24 23:52:40.665689
406	Latitude	42.3	63	7	\N	2015-03-24 23:52:40.666389
407	voooolllcoool	42.3	\N	\N	406	2015-03-24 23:52:40.667045
408	uncool	42.3	63	7	\N	2015-03-24 23:52:40.667769
414	Longitude	43.2	63	9	\N	2015-03-25 00:13:12.406711
415	Latitude	42.3	63	9	\N	2015-03-25 00:13:12.413087
416	voooolllcoool	42.3	\N	\N	415	2015-03-25 00:13:12.41383
417	uncool	42.3	63	9	\N	2015-03-25 00:13:12.414647
421	Latitude	42.3	63	11	\N	2015-03-25 00:13:40.808574
422	uncool	42.3	63	11	\N	2015-03-25 00:13:40.820047
\.


--
-- Name: contexts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: linkeex
--

SELECT pg_catalog.setval('contexts_id_seq', 423, true);


--
-- Data for Name: persons; Type: TABLE DATA; Schema: public; Owner: linkeex
--

COPY persons (id, name, "timestamp", modified) FROM stdin;
63	Tim	2	2015-03-24 23:24:13.684376
63	Tim	3	2015-03-24 23:24:29.14698
63	Tim	4	2015-03-24 23:51:35.669839
63	Tim	1	2015-03-24 22:43:48.289036
63	Tim	5	2015-03-24 23:52:12.738128
63	Tim	6	2015-03-24 23:52:26.979177
63	Tim	7	2015-03-24 23:52:40.658517
63	Tim	8	2015-03-25 00:12:59.837717
63	Tim	9	2015-03-25 00:13:12.406711
63	Tim	10	2015-03-25 00:13:26.022779
63	Tim	11	2015-03-25 00:13:40.808574
63	Tim	12	2015-03-25 00:13:46.125429
63	Tim	13	2015-03-25 00:13:50.052754
\.


--
-- Name: persons_id_seq; Type: SEQUENCE SET; Schema: public; Owner: linkeex
--

SELECT pg_catalog.setval('persons_id_seq', 261, true);


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

