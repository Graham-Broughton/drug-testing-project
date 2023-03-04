# BC Illicit Drug Testing <!-- omit in toc -->

## By Jessica Moloney & Graham Broughton <!-- omit in toc -->

<br>

### **Table of Contents** <!-- omit in toc -->

- [Summary](#summary)
  - [Main Files](#main-files)
  - [Supporting Scripts](#supporting-scripts)
- [Results](#results)

### Summary

In this project we investigate illicit drug use in BC through information scraped from the web. It is a compilation of free/low cost services across BC where individuals can bring in a sample to be identified. Fourier Transform Infrared (FITR) Spectroscopy is the main method of identification but immunoassay strips are also used to verify the presence/absence of fentanyls and benzodiazepines. Fentanyls & benzodiazapines are known to increase morbidity when present in drugs and can be present below the threshold that FITR can detect which is why the immunoassays are conducted, they have a higher specificity and sensitivity. We present a easily and highly configurable web scraper along with our analysis of the scraped data in the form of a html dashboard.

#### Main Files

This project is set up in such a way thet you only need to run one file - main.py - for scraping and another file - app.py - for the dashboard. The scraper is highly configurable with options such as multiprocessing & number of workers, wait times for web elements and number of times to retry connecting; these options are controlled from a dataclass in a single file - config.py.

#### Supporting Scripts

All python scripts for the scraper are found in "src". The web crawler is broken into three classes: CrawlerBase, PageLoader and Worker. CrawlerBase is the parent class containing the code to connect and navigate to the correct part of the webpage. PageLoader extracts the number of pages in the table, the table updates irregularly so it is necessary to find this number. Lastly, Worker does the actual scraping and is where the multiprocessing feature exists. The "data" directory contains scripts that implement the crawler as well as process the scraped data. This directory and the rest have descriptive names that do not need further explanation.

### Results

