# P15 rollback model

This slice changes only repository code/docs/CI on a feature branch. It does not mutate production systems or external data. Before merge, rollback is branch/PR rejection. After merge, normal Git revert can restore the prior language contract if verification later reveals a regression.
