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
of transforming JSON into python objects
called dataclasses.
There is [a section on dataclasses](#dataclasses)
later on that you should look at.

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

## Dataclasses

The "dataclasses" can be thought of
as the types that codegen exports.
They are used by codegen and the outside world
and are stored in `worlds/crsosscode/types`.
These are not the Archipelago-specific interfaces
mentioned in the introduction.
Codegen does not turn logic JSON
into Archipelago `Item` or `Location` instances;
rather, it turns them into these dataclasses,
which are then referenced
by CrossCode's subclasses
of `Item`, `Location`, et al.

### `ItemData` and `SingleItemData` (`types/items.py`)

In the CrossCode APWorld,
there is an assumption baked in
that you can give a player more than one
of a specific in-game item
from one Archipelago item.
For this reason,
details about items are split
across two classes,
`ItemData` and `SingleItemData`,
with `ItemData` being basically
a container for `SingleItemData`
with a quantity attached.

Item-specific details
such as name, internal CrossCode item ID, and classification,
are stored on the `SingleItemData` structure
while functional and Archipelago-specific details
are stored on the `ItemData` structure.
`ItemData`, aside from holding a quantity,
is the only class to hold a reference
to the Archipelago item ID,
which is associated with
the item and its quantity.

For items that do not map directly to vanilla items,
this is just another layer of complexity
that could and maybe should be addressed
in a different way.

#### Brief detour: rationale

There are 676 items in the game.
Normal CrossCode Archipelago item ids
begin at `B=3235824100`.
If you want to give the player
a specific quantity `q` of a normal item
with id `i`,
you give them an instance of
the Archipelago item with id `B + 676q + i`.

There were originally 100 "reserved" slots,
3235824000-3235824099,
which would be for storing items
that aren't "real" items
and are instead constructs of the randomizer,
such as elements or progressive items.
These days, there are way more
of these virtual items.
That's because of the dynamic ID system.
by telling the codegen to `__get_or_allocate_id`,
it will give you an ID in the range of 3235924000+
(100000 above the base ID).

### `LocationData` and `AccessInfo` (`types/locations.py`)

This side of things
is a lot simpler than items.
All location IDs are dynamic.
`name` and `code` are Archipelago constructs
while `area` (correlating with internal area names),
and `metadata` (which describes whether to include the location)
are constructs of the CrossCode APWorld.

One interesting aspect of the LocationData
is `AccessInfo`, which stores a combination
of region and conditions.
These are separated into their own classes
because the same construction
of region and condition
pop up all over the place in rando
(i.e. for shops).

### Conditions (`types/condition.py`)

Conditions are the backbone of logic.
CrossCode rolls its own conditions system,
which are parsed from the array synax
that you may have seen before:

```json
"condition": [
  [ "cutscene", "Talatu Introductions" ],
  [ "item", "Disc of Flora", 1 ],
  [ "botanics", 0.25 ]
],
```

These are parsed into something like this:

```python
[
	LocationCondition(location_name='Talatu Introductions'),
	ItemCondition(item_name='Disc of Flora', amount=1),
	BotanicsCompletionCondition(amount=0.25)
]
```

Each condition is expected to have the `@dataclass` decorator
so that its parameters can be set using the predictable dataclass initializer syntax.

(Note: this section describes the state of affairs after
CodeTriangle/Archipelago#24,
which is not merged as of time of writing,
but is slated to be merged).

In base Archipelago,
location conditions are set
using `Location.access_rule`,
which is of type `Callable[[CollectionState], bool]`
(if you're more familiar with JS syntax,
that is equivalent to saying `(CollectionState) => bool`).

In CrossCode, these condition classes provide
the access rules using context from the world
by way of the `satisfied` method,
which returns a `Callable[[CollectionState], bool]`,
the same type as Archipelago itself uses for access rules.
But the `satisfied` method has access to
`player`, the integer representing the current player's slot,
which is used for calls
such as `state.has(item, player, quantity)`,
`location`, the ID of the location in question,
and `args`, which is an instance of `LogicDict`,
itself a distillation
of CrossCode-specific and slot-specific details.

You are advised to do as much as possible,
including anything that is not specific to the world
or the passed `CollectionState`.
before constructing the return lambda
to avoid redundant work.

### `RegionConnection` and `RegionsData` (`types/regions.py`)

These classes, predictably,
model the region graph.
Not much needs to be said about the classes themselves,
but there is another detour to be had.

#### Brief detour: logic modes

One distinctive CrossCode feature
is logic modes.
Previously,
two logic modes were supported:
Linear and Open.
Linear logic is deprecated now,
but the framework allowing
for any number of independent
logic implementations to coexist
still remains in the code.
That is the main reason
that `RegionsData` is its own class.

## Jinja templates

Here's what you need to know
for creating a new template file.

First, make sure to start it with:
```python
{{generated_comment | indent("# ", True)}}
```
This will add a scary warning so that people don't edit it.

Okay, the real interesting thing to discuss here
are the new filters
added by the CrossCode Jinja Extension.

Take this line of code:
```python
locations_data = {{locations_data | emit_list("location") }}
```

How should we interpret this?

Well, this takes `locations_data`,
which is a `list[LocationData]`,
and transforms it into a textual representation
of a list of `LocationData`,
all in one call,
looking something like this:
```python
locations_data = [
    LocationData(code=3235824002, name='Wasteland: Storage Basement', area='arid', access=AccessInfo(region={'linear': '22', 'open': 'open18'}, cond=[ChestKeyCondition(default_level='Default')])),
    LocationData(code=3235824003, name='Wasteland: Crimson Lake Upper', area='arid', access=AccessInfo(region={'linear': '22', 'open': 'open18'}, cond=[ChestKeyCondition(default_level='Default')])),
    ...
]
```

This is handled by the `emit_list` filter,
which takes an argument
which references an AST transformer
defined by `codegen/ast.py`
(or `constant` or `tuple`,
both constructs of python's AST library).
Any function in that file
prefixed by `create_expression_`
is a transformer
that turns a dataclass of some kind
into an AST expression.
So, this call to emit_list
passes each element of `locations_data`
into `create_expression_location`,
producing an AST object
which can be stringified.

Similar filters exist for other collections
such as `emit_set`, which functions identically
but produces a set,
and `emit_dict` (which does not take a dict
but rather a `list[tuple[key, value]]`).

If you are writing code
that references items or locations,
DO NOT use the `item` or `location` transformers
as this will create duplicate instances
of the `ItemData` and `LocationData` classes
that back them.
Instead, use `item_ref` and `location_ref`
to reference the instances
declared in `items.py`
and `locations.py`
(just make sure to import them in the template).

If you have to deal with
the internals of this system,
the `ast.py` class
*should* give you enough information
to understand what's going on.
Just don't get rid
of the `fix_missing_locations` call.

One guideline:
Do try to keep things brief. This is all
going to go into source control
and possibly be overwritten many times.
Those diff bytes will eventually add up.
Use default parameters
on your dataclasses if possible
and don't set those parameters
if they are the default value.

### Broken templates

If you break a template, do not worry!
The CrossCode APWorld is built specifically
to be resiliant and not crash the codegen
if errors occur when loading the APWorld.
Just fix the template
and it should start loading again.

## After codegen (`world_data.py`, `types/world.py`)

Now, let's assume you just added a new template
or a new element to an existing template
and you want to use it in APWorld code.
If you were to simply import that module
and use the definition from there,
that would work in the majority of cases
but it would break the guarantee made
in the previous section
that errors derived from broken templates
do not cause generation to fail.

Instead, I circumvent all of this
using the `WorldData` class.
All generated elements are placed
into an instance of `WorldData`
instead of being used directly.
This is for two reasons:

1. First, the instantiation
of a `WorldData` instance
can be placed in a try-except block
so that any error occurring
throughout the process
is not fatal to the loading of
the `world.crosscode` module.
(Note that errors due to an uninitialized `WorldData`
are still caught early
in the generation phase,
if a generation is attempted.)

2. Second, this allows some flexibility
with the source of the `WorldData` instance.
Currently, alternate methods of producing
a `WorldData` instance are unimplemented,
but theoretically, it would be possible
to construct a `WorldData` from a `ListInfo`
and skip the intermediate step of writing
to files after codegen.

So, if you add variables or files
to be created by codegen,
make sure to modify the type definition
of the `WorldData` class
and the instantiation of that class
in `world_data.py`.
