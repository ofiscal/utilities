# from ofiscal_utils.draw.examples import a_cdf

if True:
  import pandas as pd
  #
  import matplotlib.pyplot as plt
  import ofiscal_utils.draw.draw as draw


def a_cdf ():
  data = pd.Series ( [1,2,7,2,7] )
  df = pd.DataFrame( data, columns=["x"])
  draw.cdf( df["x"] )
  plt.title("The empirical CDF of the observed series " + str(data) )
  plt.xlabel("Outcome")
  plt.ylabel("Probability")
  if True: # alternatives
    # plt.show() # Probably works from Jupyter and not the command line.
    plt.savefig("test-cdf.png")
  plt.close()
