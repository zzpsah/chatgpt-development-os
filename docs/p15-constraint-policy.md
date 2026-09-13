# P15 negative-constraint policy

Negative instructions narrow authority and scope. Examples: `deploy mat karna`, `delete mat karna`, `merge mat karna`.

The language layer emits these as structured constraints. Downstream routing must preserve them. A later generic phrase such as `kar do` inside the same interpreted request does not cancel an explicit negative constraint.
