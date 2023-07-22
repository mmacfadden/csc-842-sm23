# Introduction
The DB Scavenger tool allows users to search large database for sensitive data like email address, Social Security Numbers, API Keys, Private Keys, etc.  The tool was inspired by [Truffle Hog](https://github.com/trufflesecurity/trufflehog), which tries to detect sensitive data being checked into a source code repository like GitHub.

The tool supports both SQL and NoSQL databases such as PostgreSQL, MySQL and MongoDB.  The tool will search all tables, collections, documents, etc. in the database looking for interesting data and report back to the user which tables / collections contain which types of interesting data. The tool will also allow the user to extract the data from the tables / collections of interest.

# Interest / Motivation
I have had occasions to need something like this on both the offensive and defensive side of things.  On the offensive side of things, if you have gained access to a target database that is fairly large, it can be tedious to look through the entire schema looking for items of interest.  Often times there are obvious table / collection names like "Accounts" or "Users" to look for to find credentials.  But other high value data is often tucked away in non-obvious places. Things like API keys, certificates, etc. can be in less predictable table / collection names.  So having an easily extendible tool that can rapidly look through the database is handy for finding where items of interest might be.

On the defensive side, I can not tell you how many times I have seen junior (and senior) devs prototype applications and services and put things like API keys and certificates in the database in plain text.  So this tool can also be used to scan staging / production database to see if any of those bad habits have leaked into a production system where secrets are being stored unprotected.

Finally, I work across a lot of teams, companies, and projects.  So I run into a lot of different databases.  So when I get to a knew database, I always have to spend a bunch of time remembering the specific query /stored procedure syntax to do something like. So a system like this will save me a lot of time learning / relearning.


# Three Main Ideas
The three main ideas for the project are as follows:

1. **Unprotected Secrets**: (Most) developers are savvy enough to make sure that passwords are securely hashed within databases. However, we see a lot of other data being stored in the clear.  Phone numbers, SSNs, SSH Keys, API Keys, etc. often find their way into Databases in the clear.  This represents low hanging fruit for attackers to exfiltrate data.

2. **Abstracting Search and Extraction**: The main objective was to automate the process of searching through the database and optional extracting data.  The tool automates this, but also makes the command line experience the same regardless of which database you are working with.

3. **Extensibility**: The tools needs to be extendible to handle many more Databases and must also be easy to add new patterns of data to look for.  While the initial implementation is mostly based on RexEx pattern matching, the tool also needs to support more complex data identification (see below for API Key validation).  For example, if we think we found a Javascript Web Token (JWT) based on a pattern, we may want to try to parse the JWT to verify it's actually a JWT by trying to parse it.


# Future Directions
The main future features I see based on where the project is today are:

  * **API Key Validation**: API Keys are often just medium size strings of alpha numeric characters without a lot of other defining characteristics.  So if two different services have 25 digit alpha numeric API keys it would be hard to 1) detect them as interesting or 2) tell which service it is.  A secret detector could match a RegEx for a candidate API key, and then actually reach out to the service and try to authenticate to that service. If the authentication work, then we know its an API key for that service.
  * **Search Profiles**: As the list of secrets that can be detected becomes larger, the tool will become more inefficient (especially if we are making HTTP requests).  I'd like to add an optional configuration option or file which specifies which secrets to look for.  If I know what secrets an app or services is using then I can narrow down the search space.
  * **Multi-Threading**: This tool is a good candidate for multi-threading.  Each table in the database could easily be search in a separate thread, or more likely by having a thread pool process the list of tables.  This could increase the search speed for large databases.
  * **RegEx Config File**: The ability to provide a simple YAML file that contains additional patterns to search for.
  * **Authentication Flexibility**: Right now the tool assumes username and password authentication for the databases.  Some databases can be configured for other types of authenticate methods, that I would like to support.
  

# Source Code
The source code is located on GitHub hat the URL below.  The repository's README contains additional technical details about the project.:

https://github.com/mmacfadden/csc-842-sm23/tree/master/cycle-10/


# Video
A demonstration / walkthrough video has been posted to YouTube here:

https://youtu.be/Ub7mYhkB3eE
