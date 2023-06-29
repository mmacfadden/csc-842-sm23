# Introduction
The TLS Certificate Analyzer looks through packet captures looking for TLS handshakes. When a handshake is found the server certificates are extracted and evaluated. The tool provides information on all certificates exchanged in the packet capture and reports on any certificates with issues. The tool will also reach out to other threat intelligence services to get information on the IPs and Hostnames for the servers involved in the TLS exchange. The tool will provide output in a number of human-readable and/or machine-readable formats promoting integrations with other tools.


# Interest / Motivation
In my work, we call a lot of APIs for both internal and external services. Setting up certificate trust stores for internal and external APIs is often a pain for developers (especially in languages like Java). What often happens is that developers just turn off SSL / HTTPS validation when developing integrations, and never turn them back on. What this means is that there are services making outbound connections to external APIs that are not being validated from a TLS standpoint. This makes these API calls susceptible to man-in-the-middle attacks.

Trying to detect all of these in code reviews is hard and they sometimes slip through.  I have found the only way to really detect these is by monitoring traffic and looking for invalid, untrusted, or otherwise suspicious certificates.

Yes, one could do this by setting up firewalls, and things like Suricata, etc.  But many teams don't do this.  This approach just requires you to have WireShark (or some other means of capturing packets) and this script.  It's pretty quick and light weight.


# Three Main Ideas
The three main ideas for the project are as follows:

1. **TLS Certificate Validation**: Certificates are an important component of the TLS protocol. There are many reasons why a Certificate may be invalid or unacceptable. This includes self-signed certs, expired certs, certs with weak algorithms, certificates that don't cover the hostname being requested, and certificates with an untrusted intermediate or root certificate. The goal of the project is to evaluate the TLS exchanges and detect certificates with issues that might suggest either a vulnerability or an active attack.

2. **pyshark / tshark**: Many of us are familiar with Scapy as it was used in the Cyber Operations classes. Several projects in this class have made use of Scapy. Tshark / pyshark is another great way to deal with live and captured traffic. Tshark is essentially a command-line version of WireShark, and pyshark is a wrapper around it. So part of my motivation for this class was to introduce folks to PyShark / TShark if they had not seen it before.

3. **Output Generation**: I wanted to give special attention to the output of this tool, and generated three different output approaches:
  a. **Text**: This quick and dirty output prints in plain text and is intended to be saved to be printed to the console.
  b. **JSON**: Outputs results in JSON so that they could be ingested by another tool in a tool chain.  Makes sense to either print to the console (in the case of piping) or save to a file.
  c: **HTML**: This is a more human readable format, which creates a webpage with more user friendly formatting and additional details.  This is intended to be saved to a file.


# Future Directions
TBD. The main future features I see based on where the project is today are:

  * **Moment In Time Validation**: Right now the tool check expiration and validity as of the current time. Since it is a PCAP, we might be analyzing packets at a much later time when the certificate is not longer valid, even though it might have been when the packets were captured.  It would be better to be able to do "moment-in-time" validation, where we examine validity as if it were in the past.
  * **Improved Validation Logic**: The validation logic essentially bails out at the first error.  For example, the certificate might be self-signed and expired.  In this case, only the expired error will be returned.  It would be best if all of the issues related to the certificate were displayed, not just the first one.  This will require doing some validation steps manually, as the current utility class we are using throws exceptions when errors are encountered and then stops validating any further.
  * **Live Capture**: PyShark / tshark both support live capture as well.  The logic could be updated to perform live tracking.  The report generation would have to move from batch to streaming.  For JSON and Text this is pretty trivial. However, for the HTML report it would likely required standing up a websocket server to stream updates to the page.  Definitely possible, but out of scope for this cycle.
  * **Integrations Improvements**: I integrated with CrowdSec and Virus Total. I'd like to provide additional integrations to other threat intelligence services / APIs.  I also think it might be more efficient to only reach out to threat intelligence sources for only those certificates that have issues, rather than for all certificates.  It's less interesting to get a report on a valid trusted certificate, and those calls still take time.
  

# Source Code
The source code is located on GitHub hat the URL below.  The repository's README contains additional technical details about the project.:

https://github.com/mmacfadden/csc-842-sm23/tree/master/cycle-6/


# Video
A demonstration / walkthrough video has been posted to YouTube here:

https://youtu.be/TBD
