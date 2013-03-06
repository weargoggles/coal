coal
====

Coal is supposed to be straightforward. A collection of processor scripts, in any language, are located in
the COAL_PROCESSOR_DIR, by default the 'processors' subdirectory of the COAL_CONFIG_DIR (/etc/coal).

Processors output their configuration when invoked with `--host-config` and `--aggregate-config` arguments, which includes
categories,

Coal generates graphite URLs by feeding every leaf node of a carbon Store to each processor in turn. Everything except
the timebase, which is generated on rendering.

