# The Codegen Document

Updated as of **17 Jun 2026**.

'Sup. You wanna learn the secrets of the codegen?
Thought so. Strap in.

## Codegen: What's it good for?

Archipelago has a set of defined interfaces
(defined in `BaseClasses.py`)
that we need to produce
so that it knows how to generate
a CrossCode world.
Among these are:

* The `World` object;
* `Location` objects, which specify a name, id, and access condition;
* `Region` objects, for locations that have shared access conditions;
* `Item` objects, which are items that can be placed at `Location`s.

In a small APWorld these can just be instantiated
in a big list using class constructors.
However, most long-running APWorlds
find that it becomes cumbersome
to define all of their locations this way.

CrossCode outgrew this thought process
almost immediately.
Instead, we use the logic JSON
(found in `CCMultiworldRandomizer:data/in`)
to generate static python definitions
ahead of time.
These definitions,
not the code used to create them,
are included in the distributed APWorlds.

The python class definitions
are significantly more verbose,
more error-prone to type,
and overall less user-friendly
than the logic JSON,
which overall is pretty obvious
and leaves very little margin for error.

## Data used by codegen

You will need to link data files
into the `worlds/crosscode/data` directory
for codegen to work.
These are:

* `worlds/crosscode/data/in`: Link this to `CCMultiworldRandomizer:data/in`
* `worlds/crosscode/data/out`: Link this to `CCMultiworldRandomizer:data/out`.
  This directory will be written to by the codegen,
  but it also contains two "loopback" files (`items.json` and `locations.json`)
  which are both input to and output from the codegen process.
* `worlds/crosscode/data/assets`: Link this to your `assets` folder
  from your legally-obtained copy of CrossCode.

## The entry point

To run the codegen, you use:

```sh
python worlds.crosscode.codegen
```

which calls `worlds/crosscode/codegen/__main__.py`.

You can investigate that file if you want.
There are some interesting
command line arguments there.
But I'll go over the full process here.

## An overview of the process

The steps to a typical run
are as follows:

1. Merge all of the input data files
(`CCMultiworldRandomizer:data/in`)
into one master dictionary of logic JSON.

2.

## A rundown of the classes and functions

(All paths relative to `worlds/crosscode` unless otherwise specified.)

### `Context` (`codegen/context.py`)

The `Context` class
loads all of the input data,
the loopback output data,
and certain game data
(typically in JSON format).

An instance of `Context`
will be referenced by basically all
of the other codegen classes.

Among its interfaces are
`rando_data`, which refers
to the merged logic JSON;
`database`, which is loaded
from CrossCode's `database.json`;
and `item_data`, which is loaded
from CrossCode's `item_database.json`.

### `ListInfo` (`codegen/lists.py`)

The `ListInfo` class does most of the job
of transforming JSON into python objects.
These are not the interfaces mentioned
in the introduction;
instead they are custom objects
that will be referenced
by CrossCode's implementation
of those interfaces
(see [the section on dataclasses](#dataclasses)
for more information on that).

This is a large and arguably bloated class
that contains dicts and lists
that store mappings
of basically anything to anything else;
for instance, location names to `LocationData` instances
and item names and quantities to `ItemData` instances.
A lot of time will be spent in this class.

### `JsonParser` (`codegen/parser.py`)

This class also does some translation
of logic JSON to python structures.
These methods were separated because
they are pure functions that do not affect
the state of the `ListInfo` class.
Things like parsing conditions
are done by this class.

### `FileGenerator` (`codegen/gen.py`)

This class takes codegen [dataclasses](#dataclasses)
and writes them out to python files
using [Jinja](https://jinja.palletsprojects.com/en/stable/) templates.
These classes are then referenced
by the generator when creating a CrossCode world.

It also creates the [output data](#data-used-by-codegen)
which is used by both future runs of codegen and the mod.

### `CrossCodeJinjaExtension` (`codegen/jinja.py`)

This class provides several utility functions
to be used by Jinja as filters
for producing generated python definitions.
These rely on the `codegen/ast.py` module.

### AST Transformers (`codegen/ast.py`)

This module
provides different functions
that turn dataclasses
into abstract syntax trees,
which can in turn be transformed
into text.

Ideally, no one but me will ever
have to deal with the intricacies
of this module.
What you need to know
is that you use this indirectly in Jinja templates.
