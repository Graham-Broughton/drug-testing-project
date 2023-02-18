# BC Illicit Drug Testing

## By Jessica Moloney & Graham Broughton

<br/><br/>

### **Table of Contents**

- (Summary)[]
- (Project Overview)[]
  - (Main Files)[]
  - (Supporting Scripts)[]
- ()[]

### Summary

In this project we investigate illicit drug use in BC through information scraped from [bc drug checking](https://drugcheckingbc.ca). It is a compilation of free/low cost services across BC where individuals can bring in a sample to be identified. Identification is conducted using Fourier Transform Infrared (FITR) Spectroscopy and logged with what the substance was supposed to be, along with various qualitative characteristics. Fentanyl & benzodiazapines are known to increase morbidity when present in drugs and can be present below the threshold that FITR can detect. So, further testing is done for their presence using higher sensitivity test strips. Here, we present a highly configurable web scraper catered for this website to automatically generate visuals and an analysis from the scraped data.
<br/><br/>

### Project Overview

#### Main Files

This project is set up in such a way thet you only need to run one file - main.py - for scraping and the accompanying visuals and analysis. The scraper (and project in general) is highly configurable with options such as multiprocessing & number of workers, wait times for web elements and number of times to retry connecting; these options are controlled from a dataclass in a single file - config.py.

#### Supporting Scripts

All python scripts are found in "src". The web crawler is broken into three classes: CrawlerBase, PageLoader and Worker. CrawlerBase is the parent class containing the code to connect and navigate to the correct part of the webpage. PageLoader extracts the number of pages in the table, the table updates irregularly so it is necessary to find this number. Lastly, Worker does the actual scraping and is where the multiprocessing feature exists. The "data" directory contains scripts that implement the crawler as well as process the scraped data. This directory and the rest have descriptive names that do not need further explanation.

### Results

