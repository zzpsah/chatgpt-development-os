# P15 architecture position

`human utterance -> v2 interpreter -> project/context resolution -> workflow/controller -> authorization/Security Gate -> runtime -> adaptive verification -> persistence`

The interpreter is deliberately upstream and non-executing. P13 orchestration and P14 verification/healing remain downstream independent controls.
