# P15 verification plan

Fresh CI must prove all of the following before P15 can close:

1. existing Human Language Engine contract remains valid;
2. v2 contract verifier passes;
3. direct/contextual interpreter regression cases pass;
4. messy-language corpus passes;
5. safety invariant cases prove authorization stays unchanged and execution stays none;
6. the existing broader DevOS contract suite remains green.

Failure of any required check blocks completion. Passing interpretation tests does not prove downstream application behavior; it proves only the bounded language-routing contract.
