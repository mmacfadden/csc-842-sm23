# Introduction


# Interest / Motivation
Domain Generation Algorithms are a core part of malware command and control. Domain Generation Algorithms can be hard to craft, and hard to craft well.  They must be deterministic, but hard to predict.  They need to change quickly, but must allow enough time for authors to register domains. DGAs need to evolve over time, since malware researchers may develop methods (e.g. regex) that can identify the pattern associated with the DGA.  Thus the goal of this project was to provide a tool that could allow the easy generation of high quality DGAs.  This increases the maneuverability of offensive operations.  For example, it would become very easy to send out multiple variants of malware with different DGAs, such that if one DGA gets blocked, an entire bot net might not be taken down.

In addition, as a software developer by trade, I am generally interested in tools that can automate repetitive work. In prior classes at DSU, I have had to develop several DGAs. It is always tedious and I do it infrequently enough where I have to relearn how to do it each time.  Thus, this tool simplifies a required part of developing a malware C2 channel allowing me to focus on the specific requirements of the Malware system versus basic infrastructure.


# Three Main Ideas
The three main ideas for the project are as follows:

1. **Polyglot DGAs**: The project allows for generating the same DGA in multiple languages.  This is useful in two ways. First, this tool can produce DGAs for different types of malware that are written in different languages.  Second, it is sometime the case that the C2 infrastructure that might automate domain registration may be written in a different language than the malware itself.  This tool would allow generating consistent DGAs for different parts of the malware system. 

2. **Extensibility**: The project allows for extensibility in multiple ways.  Additional programming languages can be added over time.  A key part of a DGA is getting a deterministic, but hard to predict (far in advance) seed value.  Common approaches are things like the top trending twitter hash tag, etc.  The DGA Builder allows for adding plugins with different approaches for getting the DGA seed.  The other main component is how the domains are generated.  The DGA Build currently supports two methods 1) random characters, and 2) rand words from a word list.  The DGA Builder also allows for plugins to be added that create additional ways to generate domain names.

3. **Configurability**: The DGA Builder allows the user to specify the how the DGAs are built.  The goal of the project was to make it highly configurable.  For example, the user can specify the set of top-level domains to generate domains with in.  It also allows the user to configure how often the domains rotate. The seed plugins and domain name plugins all also support configurations the change how the domains will be generated.  This allows for easy creation DGAs that will behave differently, even if the same plugins are used.  Additionally, the DGA builder configuration is deterministic in that if the tool is supplied the same configuration, it will produce the same DGA.


# Future Directions
Given only about a week to work on the tool, there are a lot of opportunities for improvement.  In general documentation, error handling, and testing could be improved.  However, in terms of future functionality there are five main areas of improvement:

  * **Additional Languages**: Currently only JavaScript and Python are supported as output languages.  Adding VBA and other language support would be useful.
  * **Additional Seed Plugins**:  Additional methods to generate obtain seed values should be added over time.
  * **Additional Domain Plugins**: Additional methods to generate domain names from the seed value should be added over time.
  * **Pseudorandom Utilities**: Currently, each domain code generation plugin implements its own way to randomly generate a domain from it's corpus of characters, words, etc.  There are several deterministic pseudorandom algorithms that will provide better performance and reduce redundant code.  The leading candidate is an xorshift approach (https://en.wikipedia.org/wiki/Xorshift).  There is a UtilsCodeGenerator module already in the DGA Builder that can add helper methods such as this.
  * **Obfuscation Automation**: While the tool itself does not provide obfuscation of generated code, most languages have tools for obfuscation. It would be great if the DGA Builder could automate using the language-specific tools to optionally obfuscate the code.

# Source Code
The source code is located on GitHub here:

https://github.com/mmacfadden/csc-842-sm23


# Video
A demonstration / walkthrough video has been posted to YouTube here:

https://youtube.com