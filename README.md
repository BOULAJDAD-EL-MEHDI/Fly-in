# Fly-in Parser Documentation

This project reads a map configuration file, validates it, and converts each meaningful line into a structured object. The parser is built around a small pipeline:

1. Read the configuration file.
2. Remove comments and empty lines.
3. Detect the key of each line.
4. Choose the correct parser.
5. Parse the line into a data object.
6. Validate the overall map structure.
7. Return the parsed configuration as a list of objects.

> In the current implementation, the parser does not return one giant single object. Instead, it returns a list where each element is one parsed part of the map such as `nb_drones`, a hub, or a connection.

---

## 1. How the parser works

The main flow starts in [main.py](main.py).

### Execution flow

1. [main.py](main.py) calls `ParserEngine(config_path)`.
2. [parser_engine.py](parser_engine.py) opens the file and reads it line by line.
3. Each meaningful line is cleaned by removing comments and whitespace.
4. The first part of the line (before `:`) is used as the key.
5. [parser_factory.py](parser_factory.py) selects the correct parser for that key.
6. The chosen parser creates a configuration object.
7. [parser_engine.py](parser_engine.py) validates the relationship between parsed elements.
8. The final result is a list of parsed objects.

---

## 2. File-by-file explanation

### [main.py](main.py)
Role:
- Entry point of the program.
- Uses the parser engine on the configuration file.
- Prints each parsed item.

What it does:
- Reads the file path `config.txt`.
- Creates a `ParserEngine` instance.
- Prints the parsed configuration list.

---

### [parser_engine.py](parser_engine.py)
Role:
- The main orchestrator of the parsing process.
- Reads the file and manages the full validation process.

What it does:
- Opens the configuration file.
- Removes comments and empty lines.
- Reads each line one by one.
- Extracts the key name.
- Creates the proper parser from the factory.
- Validates the structure of the map.
- Ensures the required sections exist.
- Prevents duplicate and invalid declarations.
- Returns the final list of parsed objects.

Important validations performed here:
- `nb_drones` must appear first.
- `start_hub` must be defined once.
- `end_hub` must be defined once.
- Zone names must be unique.
- Connections must reference known zones.
- Duplicate connections are rejected.
- Self-loop connections are rejected.

---

### [parser_factory.py](parser_factory.py)
Role:
- Chooses the correct parser for each configuration line.

What it does:
- Maps each supported key to the right parser class.
- Supported keys:
  - `nb_drones`
  - `start_hub`
  - `end_hub`
  - `hub`
  - `connection`

---

### [base_parser.py](base_parser.py)
Role:
- Shared base class for all parsers.

What it does:
- Provides helper logic to parse optional metadata blocks written like:
  - `[zone=priority]`
  - `[color=blue max_drones=2]`
- Validates that metadata syntax is correct.
- Splits metadata pairs into a dictionary.

---

### [nb_drones_parser.py](nb_drones_parser.py)
Role:
- Parses the `nb_drones` line.

What it does:
- Reads the number of drones.
- Validates that it is an integer.
- Rejects zero or negative values.
- Returns a `NbDronesConfig` object.

---

### [start_hub_parser.py](start_hub_parser.py)
Role:
- Parses the `start_hub` line.

What it does:
- Reads the start zone name and coordinates.
- Validates the name format.
- Parses optional metadata such as `color` and `max_drones`.
- Returns a `StartHubConfig` object.

---

### [end_hub_parser.py](end_hub_parser.py)
Role:
- Parses the `end_hub` line.

What it does:
- Reads the end zone name and coordinates.
- Validates the name format.
- Parses optional metadata such as `color` and `max_drones`.
- Returns an `EndHubConfig` object.

---

### [hub_parser.py](hub_parser.py)
Role:
- Parses lines starting with `hub`.

What it does:
- Reads the zone name and coordinates.
- Validates the zone name.
- Parses optional metadata:
  - `zone`
  - `color`
  - `max_drones`
- Returns a `HubConfig` object.

---

### [connection_parser.py](connection_parser.py)
Role:
- Parses connection lines.

What it does:
- Reads a connection such as `hub-A`.
- Validates that it contains exactly two zones.
- Parses optional metadata like `max_link_capacity`.
- Returns a `ConnectionConfig` object.

---

### [parser_errors.py](parser_errors.py)
Role:
- Defines the custom exception classes used by the parser.

What it does:
- Groups error types by feature such as:
  - `NbDronesError`
  - `HubError`
  - `StartHubError`
  - `EndHubError`
  - `ConnectionsError`
  - `ParsingKeyError`

These exceptions make parsing failures easier to understand and debug.

---

### [colors.py](colors.py)
Role:
- Stores the allowed color values for hubs.

What it does:
- Defines an enumeration of supported colors.
- Used by the start/end/hub parsers when validating metadata.

---

### [graph_builder.py](graph_builder.py)
Role:
- Placeholder for future graph-building logic.

Current status:
- The file exists but is empty.
- It is intended to transform the parsed configuration into a graph structure.

---

## 3. Example of the parsing result

A small file such as:

```text
nb_drones: 1
start_hub: hub 0 0
end_hub: goal 10 10
connection: hub-goal
```

will be parsed into several objects, for example:
- one object for `nb_drones`
- one object for `start_hub`
- one object for `end_hub`
- one object for the connection

The final structure is a list of these objects.

---

## 4. Validation rules handled by the parser

The parser checks for:
- missing required entries
- invalid line formats
- invalid numeric values
- forbidden names with spaces or dashes
- duplicate zones
- duplicate connections
- unknown connection endpoints
- invalid metadata blocks
- unsupported metadata keys

---

## 5. How to run the parser

From the project root, run:

```bash
python3 main.py
```

The program currently uses [config.txt](config.txt) as the input file.

You can also test the parser using the provided test scripts:

```bash
python3 test_parser.py
python3 test_parser_two.py
```

---

## 6. Summary

The project follows a clean pipeline:

- Input file -> parser engine -> parser factory -> specific parser -> validated config objects -> final parsed list

This architecture makes the parser easy to extend when new map features are added.
