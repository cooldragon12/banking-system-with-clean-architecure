# Banking System with Clean Architecture

This take home project shows the clean architecture for the banking system. The files includes the possible the class and methods that can be use in banking system.

NOTE: The `main.py` file just execute the test cases for this project.

## Requirements

Only the pre-built Python libraries is needed.

- Python 3.12.3


## Execute

To test the app use this command. It outputs the account statement.
```bash
python main.py
```


## Description

### Folder Structure
**src/** - This is the main folder hold the main files

**core/** 

- Contains the domain layer such as entities.
- Also caintains the UseCase Layer

**infrastracture/**

- Contains the repository that holds and store the entities.
