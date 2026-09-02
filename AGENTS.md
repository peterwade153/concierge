## Project Domain

A Restaurant Recommendation Agent, that recommends fine dining spots in specific neighborhood. 
Uses Nominatim API to get Location Coordinates, and FourSquare API to look up restaurants within a radius of those Coordinates.

## Project Setup and Management

- Python version: 3.11.
- Dependency management: `pip` and `requirements.txt` file.
- Add a dependency with `pip install <package>`.
- Run the app with `python api/run.py`.
- Branch from `master` as `feature/<name>` and use Conventional Commits.
- Stage changes for review. Don't commit to `master` or push without being asked.

## Architecture Overview

- **agent** : Main AI restaurant recommendation module
- **api** : REST APIs to return the AI restaurant recommendations 

## Coding Conventions

- Type-hint public functions and methods, including their return types.
- Use `pathlib` for path management. Don't use `os.path`.
- Prefer f-strings over `str.format()` or `%` formatting.
- Follow EAFP: handle exceptions rather than checking conditions up front.
- Write Google-style docstrings for every public function and method.
- Validate request bodies with Pydantic models.
- Embrace idiomatic Python like comprehensions, generators, and decorators.

## Constraints

- Ask before adding any external dependency.
- Preserve the signature and response shape of existing endpoints.
- Don't use blocking I/O inside `async` functions.
- Keep existing tests intact, and fix the code to make them pass.
- Declare a task done only after the gates pass and docstrings are
  updated.

## Ignore

Treat everything in `.gitignore` as off-limits to read or edit. On top of
that, never open:

- Secrets and `.env` files
- Large data files unrelated to the current task
- Vendored or generated code
