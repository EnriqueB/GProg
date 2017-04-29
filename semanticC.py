def getResultingType(var1, var2, op):
    semanticCube = {
        int: {
            int: {
                '+'   : int,
                '-'   : int,
                '*'   : int,
                '/'   : int,
                '<'   : bool,
                '<='  : bool,
                '>'   : bool,
                '>='  : bool,
                '=='  : bool,
                '!='  : bool,
                '='   : int
            },
            float: {
                '+'   : float,
                '-'   : float,
                '*'   : float,
                '/'   : float,
                '<'   : bool,
                '<='  : bool,
                '>'   : bool,
                '>='  : bool,
                '=='  : bool,
                '!='  : bool,
                '='   : int
            }
        },
        float: {
            int: {
                '+'   : float,
                '-'   : float,
                '*'   : float,
                '/'   : float,
                '<'   : bool,
                '<='  : bool,
                '>'   : bool,
                '>='  : bool,
                '=='  : bool,
                '!='  : bool,
                '='   : float
            },
            float: {
                '+'   : float,
                '-'   : float,
                '*'   : float,
                '/'   : float,
                '<'   : bool,
                '<='  : bool,
                '>'   : bool,
                '>='  : bool,
                '=='  : bool,
                '!='  : bool,
                '='   : float
            }
        }
    }
    try:
        return semanticCube[var1][var2][op]
    except KeyError:
        raise KeyError("ERROR: KeyError in getResultingType: semanticC[{}][{}][{}]".format(var1, var2, op))
        return None
