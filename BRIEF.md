# Zendesk Search


## Description and requirements:

Using the provided data (tickets.json and users.json and organizations.json) write a simple  command line application to search the data and return the results in a human readable format.

* Feel free to use libraries or roll your own code as you see fit.  
* Where the data exists, values from any related entities should be included in the results, i.e.  searching organization by id should return its tickets and users. 
* The user should be able to search on any field, full value matching is fine (e.g. "mar" won't return "mary")
* The user should also be able to search for empty values, e.g. where description is empty. 

Ideally, search response times should not increase linearly as the number of documents grows. You can assume all data can fit into memory on a single machine.
