# P15 context source

The interpreter itself does not fetch chat history or repositories. A DevOS host supplies context after applying repository-first recovery rules. This separation keeps language interpretation portable and prevents hidden context from silently overriding Git/project evidence.
