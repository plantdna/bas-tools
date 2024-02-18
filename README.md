# BAS-Tools

> Background Assessment And Screening Tools For Simplified Markers
---

## [Click this to download BASTools.zip](https://gitee.com/bmstc/bas-tools/releases/download/V1.0.0/BASTools.zip)

## Description

The BAS-Tools consists of two functional modules, respectively Simplified Marker Design and Background Assessment. The entry data format of the tools is consistent with the Plink software using the ped and map format files, where ped files are used to store genotyping data and map files are used to store marker information data. In addition, the result data generated after the analysis are stored in the output directory of the same level as the software.

The Simplified Marker Design module is responsible for designing the simplified markers, Users need to build the ped and map files based on the genotype data of the parents, specify these files path in the software, set the Number parameter (the number of selected in each region), Then click on the "Start the analysis" button, The software will filter out the simplified markers and store the result information in a file named "selected_markers.map" under the output directory, At the same time, the software will show the distribution of simplified markers on the chromosome in a picture.

![Simplified Marker Design](https://foruda.gitee.com/images/1706247584586742233/1decaa18_1214041.png)

The Background Assessment module can evaluate the background of the population data using the simplified marker, the parameters are the path of the ped and map files, the ped file is the genotyping data of the population, where the first line is the parent by default, the population material will calculate the background response rate with the parent as the reference, and the map file is the "selected_markers.map" file generated for the Simplified Marker Design module. After clicking the "Start the analysis" button, the software will calculate the background of each material in the group, and displayed in the table form in the software, at the same time, the software will generate simulated background map for each material, when the user selected a line of data in the table, the simulation of the material will be displayed in a new window.

![Background Assessment](https://foruda.gitee.com/images/1706247604115802721/f48a50b8_1214041.png)

![Background Map](https://foruda.gitee.com/images/1706247692970199392/79018be0_1214041.png)

## How to run

```python
1. cd BAS-TOOLS
2. python -m venv venv
3. source venv/bin/activate
4. pip install -r requirements.txt
5. python index.py
6. pyinstaller bas.spec
```