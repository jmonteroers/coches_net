# CochesNetAds
[coches.net](https://www.coches.net/) is one of the most popular online markets for car transactions in Spain. This repo provides tools to read ads and identify discounts from manually-downloaded pages from [coches.net](https://www.coches.net/) (no scratching involved). The pages from [coches.net](https://www.coches.net/) need to be search results.

Reading the downloaded HTML files is done with BeautifulSoup, by identifying all ads and for each ad, extracting all present features. You can build your dataframe from all HTML search results in a folder at once. Then you can always add more ads from new pages to your database if you want, thus creating a large dataframe with all your search results! True, downloading webpages manually is boring, but is more respectful towards the owners of the webpage.

The package also offers functions to apply residual analysis to these dataframes in order to identify discounts. Basically, you can choose among several statistical models to estimate. The observations with the lowest residuals are identified as possible discounts. The intuitition for this approach is that, as far as the statistical model is concerned, a residual represents a misvaluation. The lower the residual, the larger the undervaluation according to the model.

Currently, this package is under development and most functions still need testing.
