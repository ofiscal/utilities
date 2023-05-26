def near (
    a : float, # compare this
    b : float, # to this
    tol_abs  : float = 0.001, # closer than this             => they are near
    tol_frac : float = 0.001  # differ by this ratio or less => they are near
) -> bool:
    if ( ( abs( a - b )
           < tol_abs ) |
         ( abs( a - b )
           <= (tol_frac * max( abs(a), abs(b) ) ) ) ):
        return True
    else: return False
