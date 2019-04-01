# csCommunities
##### Authors: Peter Xenopoulos, Qi Sun
###### Last Updated: 4/1/2019
The computer science research landscape has changed dramatically over the last few decades. Research interests have come and go, new has become old, and even entire research communities have formed. While there is extensive analysis of citation graphs on the author level, there is far less research at the community level. In this repository, we include both the data processing and visualization code for the analysis of computer science research *communities*.

First and foremost, our tool can uncover the changing landscape between different communities by investigating citation flows over the years. Additionally, our tool can also be used interactively to explore local structures within the graph, which can uncover subnetworks within generalized computer science research communities.

## Data
We use the citation network data from the DBLP network, which we accessed through [this link](https://aminer.org/citation). We put the data in a folder called `python/data/`, which is hidden with our `.gitignore` file. You can download and prepare the graph data by running `./install.sh`. Please note that running this script can take quite a while, as the data is large and some of the processing steps can take a bit of time. We include this functionality primarily for reproducibility purposes, as most of the graph data can be found as described below.

## Graphs
You can access archived versions of the graph in the `python/graphs/` folder.

## Visualization
The visualization for this project is located in the `web/` folder and makes uses of d3.
