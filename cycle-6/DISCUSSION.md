# Introduction
As mentioned in an earlier cycle, [Steganography](https://en.wikipedia.org/wiki/Steganography) is a technique to hide data within an another, seemingly innocuous file  order to avoid detection during transmission. The hidden data is then extracted at its destination.  It is a useful technique for data exploitation, when you need to get data out of an enterprise though a system that may have data loss prevention systems.  PDFs are very commonly sent in businesses as attachments to email.  Business and individuals commonly send/receive PDFs in the course of normal business, so PDFs are commonly accepted file formats.  What's more, PDFs can often be fairly large allowing for larger amounts of data to be moved without raising concerns.  For example, document scans can easily be 10s of MBs.

PDFs allow attaching files.  However, users can usually see that files are attached.  What's more, Data Loss Prevention systems can also identify attachments and inspect those attachments for sensitive data.  The project aims to embed files in a PDF in a way that is harder to detect, as a means to exhilarate data of an organization through email, messaging, or file sharing services.


# Interest / Motivation
Compromising end user workstations through malware is a topic of interest to me.  In recent years I have seen a lot of host based security, firewalls, data loss prevention systems, etc. start to block several C2 channels.  Corporate HTTP Proxies and the like often even have started to block large file uploads. I am always looking to build multiple ways of getting data out of an target system.  Even if https uploads work, I find it convenient to use a multitude of methods.  For one, spreading large data exfiltration across multiple methods and protocols may make it harder to detect.  Also, if one method gets locked down, other methods may still persist as an incident response team is working through the attack.

Thus, this tool just becomes one more tool in the tool belt, that would allow me to exfiltrate data through email, messaging apps (slack, teams, etc.), or file sharing sites.


# Three Main Ideas
The three main ideas for the project are as follows:

1. **Embedding Files**: The overall objective was to embed fils into a PDF.  PDFs support file links and attachments. Links simply point to other files on the filesystem (or a URL), whereas attachments are embedded directly in the document.  Thus, the PDF can act as a container for other file.  The PDF can be sent via email or messaging application without looking like other files are being sent.  Other file containers such as a Zip file are obvious file containers, whereas PDFs are a bit more subversive.  Files can be attached to any existing valid / common PDF.  If a user was to simply open the PDF they would generally just see what looks like a normal PDF.

2. **Obfuscation**: While, people might not even both to open the PDF, if they do they MAY not see the attachments.  However, most PDF viewers allow users to look at the attachments.  Thus, a goal of the tool was to hide the attachments from the user.  This is accomplished by editing the raw binary PDF file after the attachments are added.  The "tag" which identifies file attachments is modified in a way where a PDF view will essentially ignore the attached file.  This way if a user, or a data loss prevention system inspects the PDF to see if there are attachments, no attachments will be found.  This process is reversed on the receiving end to recover the files.  Additionally, the AES encryption will make it harder for an organization to detect what was exfiltrated, even after detection.

3. **Encryption**: While the data structure that lists attachments is obfuscated, the files would otherwise still be in the file.  A savvy data loss prevention tool might still be able to find signatures within the PDF file and/or detect prohibited keywords, etc.  Thus the files that are embedded in the PDF can be encrypted with symmetric AES 256 encryption.


# Future Directions
TBD. The main future features I see based on where the project is today are:

  * **DLP Testing**: I would like to test this against DLP tools to see how effective the approach is.  I've only tested against the Data Loss Prevention system built into Microsoft 365.  I was able to send prohibited files through a PDF. However, I'd like to test against a broader range of data protection tools.
  * **Higher Order Automation**: Currently the tool takes a specific set of files and embeds them in a specific PDF.  While this is a good start, many email/messaging systems have limits in the size of attachments.  I'd like the ability to do two things:
    1. I'd like to be able to supply a set of PDFs to use to embed files in, along with a larger list of files. I would like the tool to then bin pack the files to embed across multiple PDFs in an automated way.
    2. For large files, I would like the tool to be able to chunk the file into multiple compressed segments and then spread the chunks across multiple PDFs. The tool would need to be able to then reconstitute the file given the multiple PDFs on the other end.
  * **Golang Port**: I wanted to write the proof of concept in python since I know I could do it relatively quickly.  However, this is an exploitation tool that would need to be distributed into a target environment, and Python might not be the best choice, in retrospect.  First, its multiple files, which is somewhat of a pain to move across a network (yes it can be zipped).  It also requires the target system to have python, possibly pip, and requires permissions (and connectivity) to install python dependencies.  Porting this to Golang and producing a statically linked, single binary with no dependencies seem like a reasonable improvement for a tool of this kind.
  

# Source Code
The source code is located on GitHub hat the URL below.  The repository's README contains additional technical details about the project.:

https://github.com/mmacfadden/csc-842-sm23/tree/master/cycle-6/


# Video
A demonstration / walkthrough video has been posted to YouTube here:

https://youtu.be/TBD
