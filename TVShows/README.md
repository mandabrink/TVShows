"# f19-resourceful-mandabrink"

# TV Shows

## Resource

**shows**

Attributes:

* name (string)
* genre (string)
* status (string)
* rating (integer)

## Schema

```sql
CREATE TABLE shows (
id INTEGER PRIMARY KEY,
name TEXT,
genre TEXT,
status TEXT,
rating INTEGER);
```

## REST Endpoints

Name                     | Method | Path
-------------------------|--------|-----------------
Retrieve show collection | GET    | /shows
Retrieve show member     | GET    | /shows/*\<id\>*
Create show member       | POST   | /shows
Update show member       | PUT    | /shows/*\<id\>*
Delete show member       | DELETE | /shows/*\<id\>*
