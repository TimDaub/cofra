# Cofra

Cofra is a framework for recording arbitrary contextual data historically.


## Installation
Cofra uses `pip` for third-party dependency management.
To install all required Python packages, run:

    pip install -r requirements.txt

Additionally, Cofra uses PostgreSQL for saving data persistently.
We recommend installing `postgres.app` as well as an compatible SQL workbench.
As `config.cfg` contains sensitive information (for example your DB password), it is on the `.gitignore` list and will never be commited to a repository.
For your convenience, we included an exemplary version of our `config.cfg` file, called `config_example.cfg`.
Just rename it to `config.cfg` and fill in our credentials to start.

In addition, make sure you've set up Emotext correctly.

## Running Cofra
Cofra runs the main process of Emotext and itself.
To run it appropriately, the following instances should run:

1. An instance of conceptnet5 that is available via HTTP
2. An instance of PostgreSQL that is accessible via the configured parameters in `config.cfg`
3. An instance of Cofra

## RESTful web interface
All routes can be inspected inside of `wsgi/webapp.py`.
In overview, these are the routes that are available:

    Emotext
        POST, OPTIONS /texts
        POST /entities/<entity_name>

    Cofra
        GET, POST /persons
        GET /persons/<int:person_id>/versions
        GET /persons/<int:person_id>/versions/<int:timestamp>
        POST, DELETE /persons/<int:person_id>/contexts/<int:context_id>
        POST /persons/<int:person_id>/contexts

### Emotext specific routes

#### POST, OPTIONS /texts
Simple method to convert text to a emotion vector, without the structural form of an conversation. This means that EtMiddleware's clustering algorithm is not used. 

Example of a request's body:

    {
      "entity_name": "Tim",
      "text": "those are some words",
      "language": "english",
      "date": "2015-03-25T00:13:50.05275"
    }

`date` can be omitted. Right now only `english`, `german` and `french` are supported language-wise.
Please note though, that any results other than in the English language will probably be poor.

#### POST /entities/<entity_name>
This route uses MessageClustering. You can configure the threshold time in `config.cfg`. If your message was added to a conversation and the threshold time is not exceeded you get `Message added to cluster algorithm. OK.`.
Otherwise, the a fully interpreted conversation should be returned.

Example of a request's body:

    {
      "entity_name": "Tim",
      "text": "Some more words",
      "language": "english",
      "date": "2015-03-25T00:13:50.05275"
    }

`date` can **NOT** be omitted and should represent the actual time a message was composed.

### Cofra specific routes

#### GET /persons
Returns a list of all saved persons and their children/states.

Example of a response's body:

    [
        {
            "timestamp": 0,
            "modified": "2015-03-29T18:48:24.025298",
            "children": [],
            "name": "Alice",
            "id": 441
        }
    ]

#### POST /persons
Creates a person on the server. As said in the actual documentation (thesis), only one Node at a time can be created. Hence, a person-object containing children can not be created with this single request. For this, use `POST, DELETE /persons/<int:person_id>/contexts/<int:context_id>` or `POST /persons/<int:person_id>/contexts`.

Example of a request's body:

    { "name": "Alice" }

As well as the server's response:

    {
        "name": "Alice",
        "id": 0,
        "timestamp": 0,
        "modified": 2015-01-13T15:32:43.450686Z, "children": []
    }

#### POST /persons/<int:person_id>/contexts/<int:context_id>*
Once we have created a person (like in the example above), we can add contextual data to it.
For this, we can either use:

1. `POST /persons/<int:person_id>/contexts`
2. `POST /persons/<int:person_id>/contexts/<int:context_id>`

(1.) Saves the contextual data as a child of the addressed person, while (2.) saves it as the child of another contextual data.

**Adding contextual data to a person**

Example of a request's body:

    { "key": "Location" }

As well as the server's response:

    {
        "name": "Alice",
        "id": 0,
        "timestamp": 1,
        "modified": 2015-01-13T15:35:33.456586Z,
        "children": [{
            "id": 0,
            "key": "Location",
            "modified": 2015-01-13T15:35:34.656236Z,
            "children": []
        }] 
    }

Using `{ "key": "Location" }`, we have successfully added contextual data as a child to Alice.

**Adding contextual data to another context**
If we now want to add contextual data to another context, we can do this by addressing it appropriately as well:
Therefore, we need to send our request to (2.) using the correct `context_id`.

Example of a request's body:

    {
        "key": "Longitude",
        "value": "10.4541194"
    }

As well as the server's response:

    {
        "name": "Alice",
        "id": 0,
        "timestamp": 2,
        "modified": 2015-01-13T15:35:33.456586Z,
        "children": [{
            "id": 0,
            "key": "Location",
            "modified": 2015-01-13T15:35:34.656236Z,
            "children": [{
                "id": 0,
                "key": "Longitude",
                "value": "10.4541194",
                "modified": 2015-01-13T15:37:11.102655Z,
                "children": []
                }]
        }] 
    }

Note that there are now three versions of Alice, all marked with a logical timestamp.

#### GET /persons/<int:person_id>/versions
To see all versions of Alice, we can request this route and will be returned a list of versions.

#### GET /persons/<int:person_id>/versions/<int:timestamp>
Furthermore, we can also request a specific version of Alice's history by specifying the versions timestamp explicitly.