# weekAtAGlanseAPI
Uses and aggregates NCR transactions into weekly and time based patterns, frontend on https://github.com/rscsam/weekataglanse

We coded this server for HackGT5, 2018 and competed for the NCR, Microsoft, and ESRI prize.
https://devpost.com/software/weekataglanse

## Technologies used
We hosted our entire stack on Azure and used SQL Server, Python Flask for our server, and a React Frontend which queried our server.
We took transaction data from the NCR API and prepopulated/cached transactional data in the SQL Server.
We categorized transactions using the Bing Search API to find context for item names then running the contexts throught Microsoft's Intelligence services Entity Extraction API.

