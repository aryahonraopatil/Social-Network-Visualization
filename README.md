# SocialPlanet
The idea of the project is to analyze the effect of location on the network between people from all over the world by targeting the travel history of social media users and their connections. The users would be able to see how the network changes over time, travel patterns of people, possible changes in popularity over time and many more. 

![This is an image](/paper_source/figures/fig5a.jpg)

## The-Social-Planet\
├── code\
│	 ├── Generate_Dataset\
│	 │	 ├── main.py\
│	 │	 ├── networkgen.R\
│	 │	 ├── network.py\
│	 │	 └── profile.py\
│	 ├── Magic_Planet_Display\
│	 │	 ├── Magic_Planet_Display.pde\
│	 │	 ├── magicPlanetShader.glsl\
│	 │	 ├── media\
│	 │	 │	 └── mapBase.png\
│	 │	 ├── Node.pde\
│	 │	 └── zoomShader.glsl\
│	 └── Scraping\
├── datasets\
│	 ├── accounts.csv\
│	 ├── edges.csv\
│	 └── worldcities.csv\
├── paper_source\
│	 ├── figures\
│	 │	 ├── fig1a.png\
│	 │	 ├── fig1b.png\
│	 │	 ├── fig2a.png\
│	 │	 ├── fig2b.png\
│	 │	 ├── fig3.png\
│	 │	 ├── fig4a.png\
│	 │	 ├── fig4b.png\
│	 │	 ├── fig5a.png\
│	 │	 ├── fig5b.png\
│	 │	 └── fig5c.png\
└── README.md

To display the visualization on the Magic Planet, Processing is required. When plugging in the Magic Planet, make sure to set the projector to 1600x1200.
Download the repository, then open the Processing project under /code/Magic_Planet_Display/Magic_Planet_Display.pde and run it. For standalone visualization outside of the globe set the boolean standalone to true. If you wish to try zoom, set the boolean for zoom to true. Zoom is unused as it does not display correctly on standalone mode and distorts the globe in such a way that we do not recommend its use.

## Controls
Esc - quit/close
Left Arrow - rotate left
Right Arrow - rotate right
Up Arrow - rotate up
Down Arrow - rotate down
P - Toggle autorotate

## Dataset Generation
Simulated dataset
The R file provided in /code/Generate_Dataset/ will generate an artificial dataset of nodes as specified by the three parameters at the top of the file. Run this file however you wish, but we used R Studio Code. Tweaking these can provide for a more real visualization. To use a generated dataset, copy the "accounts.csv" and "edges.csv" files to /datasets and run the visualization.

## Scraping
Scraping was never completed and does not work properly. It was abandoned due to the time it takes to scrape and some unresolved issues. If you'd like to try, it requires Pandas, Geopy, Numpy and Selenium. You also need to place Chrome Driver executable in the same location as the python scripts. You'll also need account credentials to use to scrape with.

## Dependency Licenses
Processing - GPL v2
Selenium - Apache 2.0
Numpy - BSD 3
Pandas - BSD 3
Geopy - MIT

Team - Salem Soin-Voshell(salems1@umbc.edu), Warren Funk(wfunk2@umbc.edu), Dagem Sinke(dsinke1@umbc.edu), Arya Honraopatil(ahonrao1@umbc.edu), Bhargavi Poyekar(bpoyeka1@umbc.edu), Hardeep Dulkoo(hdulkoo1@umbc.edu)
