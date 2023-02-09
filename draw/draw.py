if True:
  import numpy as np
  import pandas as pd
  #
  import matplotlib.pyplot as plt


# PITFALL: Does not close the plot to further drawing.
def cdf ( series : pd.Series,
          logx = False,
          draw_mean_too = True,
          draw_pmf_too = False,
          xmin = None,
          xmax = None,
          sample_size = None,
          **kwargs ):

  data = pd.DataFrame()
  data["x"] = series . sort_values() . astype ( "float" )
  data["count"] = 1

  if True: # Define horizontal min, max, and step size.
    dmin = data["x"].min()
    if xmin != None:
      dmin = max(dmin,xmin)
    dmax = data["x"].max()
    if xmax != None:
      dmax = min(dmax,xmax)
    dstep = (dmax - dmin) / 500 # arbitrary resolution

  pmf = data . groupby("x") . agg('sum')
    # Taking the sum yields the nonzero part of the pmf.
  mass = pmf["count"].sum()
  pmf["nonzero_pmf"] = pmf["count"] / mass
  pmf = pmf . reset_index ( level="x" )
    # Move x from the index to a normal column.

  pmf_range = pd.DataFrame()
  pmf_range["x"] = np.arange (
    # Includes a 10-step (5%) buffer on each side.
    dmin - 10*dstep, dmax + 10*dstep, dstep )

  df = pmf_range.merge(
    # RELAX. Merging on floats might look crazy,
    # but in an outer merge, nothing is lost.
    pmf, on = "x", how = "outer" )
  df["pmf"] = np.where( # This is like if-else.
    df["nonzero_pmf"] . isnull(),
    0,
    df ["nonzero_pmf"] )
  df = df[["x","pmf"]] # drop columns "count" and "nonzero_pmf"
  df = df.sort_values("x")
  df["cdf"] = df["pmf"] . cumsum()

  if logx:
    plt.xscale("log")
  if draw_pmf_too:
    plt.plot( df["x"], df["pmf"] )
  if draw_mean_too:
    mu = data["x"] . mean()
    plt.axvline( mu )
    plt.text( mu, 0,
              "mean = " + format( mu, '.2e') )
  if sample_size:
    fig, ax = plt.subplots()
    plt.text ( 0.1, 0.9,
               "n = " + str(sample_size),
               # As coordinates, use fractions of axes,
               # rather than data (which is the default).
               transform = ax.transAxes )

  plt.gca() . set_xlim ( left = dmin, right = dmax )
  plt.plot ( df["x"], df["cdf"], **kwargs )

# PITFALL: Does not close the plot to further drawing.
def single_cdf( series, xlabel, **kwargs ):
  plt.grid ( color='b', linestyle=':', linewidth=0.5 )
  plt.xlabel ( xlabel )
  plt.ylabel ( "Probability" )
  cdf( series, **kwargs )
