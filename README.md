# ultra-optimization
Using Postman Problems Repo, osmnx, and networkx to optimize and visualize a route in pacific spirit park
Code from medium article: https://medium.com/@sean.mckay.314/rural-chinese-postman-problem-ultra-optimization-using-networkx-and-osmnx-b245764db2b2

# Notes
The nodes.csv and edges.csv files were manually created using data from Gaia GPS. The waypoints are available in the file `pacific-spirit-ultra-waypoints.gpx`.
The format for the edgelist is setup to work with the `postman-problems` repo here https://github.com/brooksandrew/postman_problems/tree/master.

The final gpx `pacific-spirit-ultra-optimized.gpx` was also manually created in Gaia using the optimal circuit information

# Setup
If not already done:
 - Download and install python 3 (https://www.python.org/downloads/)
 - Download and install jupyter-lab (https://jupyter.org/) 
 - Download and install conda (https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
 - Configure ipykernel (https://ipython.readthedocs.io/en/stable/install/kernel_install.html)

# Run instructions
Clone the repo
`git clone https://github.com/sean-m-mckay/ultra-optimization.git`

Clone the postman problems repo inside this repo
`cd ultra-optimization`
`git clone https://github.com/brooksandrew/postman_problems.git`

Install the conda environment
`conda env create -f environment.yaml`

Launch a jupyter lab session
`jupyter lab`

Open the file `Postman_Pacific_Spirit.ipynb`, select the kernel `Python [conda-env: ultra-optimization]` and run all cells









