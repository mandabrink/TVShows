"# f19-resourceful-mandabrink"

# TV Shows

## Resource

**shows**

Attributes data:

* name (string)
* genre (string)
* status (string)
* rating (integer)

Attributes for user:

* fname (string)
* lname (string)
* user (string)
* password (string)

## Schema

```sql
CREATE TABLE shows (
id INTEGER PRIMARY KEY,
name TEXT,
genre TEXT,
status TEXT,
rating INTEGER);
CREATE TABLE users (
sid INTEGER PRIMARY KEY,
fname TEXT,
lname TEXT,
username TEXT );
```

## REST Endpoints

Name                     | Method | Path
-------------------------|--------|-----------------
Retrieve show collection | GET    | /shows
Retrieve show member     | GET    | /shows/*\<id\>*
Create show member       | POST   | /shows
Update show member       | PUT    | /shows/*\<id\>*
Delete show member       | DELETE | /shows/*\<id\>*
