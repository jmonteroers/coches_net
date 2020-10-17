# CochesNetAds
Read ads and identify discounts from manually-downloaded pages from [coches.net](coches.net) (no scratching involved). 

Reading the downloaded HTML files is done with BeautifulSoup, by identifying all ads and for each ad, extracting all present features. The functions of this repo allow you to either build all your database at once, or gradually build it by adding new pages to an existing database.

Once the database is constructed, residual analysis is applied to identify discounts. Basically, several statistical models are estimated and the observations with the lowest residuals are identified as possible discounts. The intuitition for this approach is that, as far as the statistical model is concerned, a residual represents a misvaluation. The lower the residual, the larger the undervaluation according to the model.
