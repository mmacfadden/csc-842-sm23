# Introduction
As mentioned in an earlier cycle, [Steganography](https://en.wikipedia.org/wiki/Steganography) is a technique to hide data within an another, seemingly innocuous file  order to avoid detection during transmission. The hidden data is then extracted at its destination.  It is a useful technique for data exploitation, when you need to get data out of an enterprise though a system that may have data loss prevention systems.  PDFs are very commonly sent in businesses as attachments to email.  Business and individuals commonly send/receive PDFs in the course of normal business, so PDFs are commonly accepted file formats.  What's more, PDFs can often be fairly large allowing for larger amounts of data to be moved without raising concerns.  For example, document scans can easily be 10s of MBs.

PDFs allow attaching files.  However, users can usually see that files are attached.  What's more, Data Loss Prevention systems can also identify attachments and inspect those attachments for sensitive data.  The project aims to embed files in a PDF in a way that is harder to detect, as a means to exhilarate data of an organization through email, messaging, or file sharing services.


# Interest / Motivation
TBD


# Three Main Ideas
The three main ideas for the project are as follows:

1. **Embedding Files**: TBD

2. **Obfuscation**: TBD

3. **Encryption**: TBD


# Future Directions
TBD. The main future features I see based on where the project is today are:

  * **DLP Testing**: I would like to test this against DLP tools to see how effective the approach is.  I've only tested against the Data Loss Prevention system built into Microsoft 365.  I was able to send prohibited files through a PDF. However, I'd like to test against a broader range of data protection tools.
  * **Higher Order Automation**: TBD.
  * **Golang Port**: I wanted to write the proof of concept in python since I know I could do it relatively quickly.  However, this is an exploitation tool that would need to be distributed into a target environment, and Python might not be the best choice, in retrospect.  First, its multiple files, which is somewhat of a pain to move across a network (yes it can be zipped).  It also requires the target system to have python, possibly pip, and requires permissions (and connectivity) to install python dependencies.  Porting this to Golang and producing a statically linked, single binary with no dependencies seem like a reasonable improvement for a tool of this kind.
  

# Source Code
The source code is located on GitHub hat the URL below.  The repository's README contains additional technical details about the project.:

https://github.com/mmacfadden/csc-842-sm23/tree/master/cycle-6/


# Video
A demonstration / walkthrough video has been posted to YouTube here:

https://youtu.be/TBD
