---
layout: post
title: Trouble with Olimex RFID cards and readers
---

There have been some reports of trouble with certain cards not being read by the Olimex reader.
Cam got in touch with DigiKey after he had to return a set of cards and they did some digging, it seems the problem is the chip inside the RFID card not matching what the reader supports.

From the [Olimex MOD-RFID125 reader user manual](https://www.olimex.com/Products/Modules/RFID/MOD-RFID125/resources/MOD-RFID125.pdf):
    - Supports Manchester-encoded 64-bit EM4102 RFID tags with 64 periods of carrier frequency per data bit;
    - Base RFID frequency 125kHz;

However, the Parallax cards we had been using apparently have support for multiple encoding methods, and which one is used in the card is often not in the supplier data.

If you choose to use an Olimex reader in your design please contact your supplier and ensure the cards you purchase will meet the requirements.  It may be that they can't guarantee this.  Cam had previously purchased more than he needed and returned the unusable cards, less than ideal but it got the job done.

In the meantime, there are some alternative readers available that might fit the bill but they have not been tested by us and there form factor might be less than ideal.
One option I came across at SparkFun was the [SparkFun RFID Starter Kit](https://www.sparkfun.com/products/13198).
It would be worth while to check suppliers like [DigiKey](https://www.digikey.com/), or to try contacting [Olimex](https://www.olimex.com) and asking if they can ensure the cards you purchase will work with the reader, though Cam has had some trouble with there customer service in the past.

Please let us know about your experience with this issue in the comments below, or check the relevant [wiki page](https://github.com/asclepius/edus2/wiki/Hardware).
