# Community Bible Study Enabler

### Requirements:
1. pandas

A python script the sends emails to the specified email ids with sending N(any number) of verses from the bible per email. The code is written such that it stars from the first verse of the book of Genesis and ends at the last verse of the book of Revelations.

This scipt creates an Simple Mail Transfer Protocol**(SMTP)** server of the senders email id and send the emails to the specified list of email addresses.

To automate it and run it as cron job on your mac or linux pc, open your terminal and type the following commands.

```bash
  crontab -e
```

By default if either opens up in nano or vim, type the following and save the file.

```bash
  0 9 * * * * python3 <path to the file>
```

This should run the script at 9:00 AM everyday. 

If on the the windows PC you can use the windows task scheduler.
