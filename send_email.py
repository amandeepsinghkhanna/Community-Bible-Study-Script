
"""
    @script-author: Amandeep Singh Khanna
    @script-description: 
"""

# importing standard python modules:
import os  # for interfacing with the operating system.
import datetime # for datetime operations.
import logging  # for creating code execution log.
import smtplib  # for creating a mailserver.

# importing PYPI modules:
import pandas as pd  # for interfacing with the pandas DataFrame objects.

# os.chdir(r"/home/pi/Desktop/bible_email_reminder")

# setting global variables:
file_path = "american_standard_bible.csv"
verse_to_send = 3
file_path = "american_standard_bible.csv"
email_id = "amankhanna1993@hotmail.com"
password = "Nikon@d3200"
server_name = "smtp.live.com"
port = 25
receiver_ids = ["amandeepsinghkhanna@gmail.com", 
"simeran.khanna@dell.com", "simerankaurkhanna@gmail.com", 
"parashar.upro@gmail.com", "jaswinder_singh90@live.com"]

# setting the logging configuration:
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(filename)s -  %(levelname)s - %(message)s ",
    handlers=[
        logging.FileHandler("bible_email.log"),
        logging.StreamHandler(),
    ],
)

# user-defined function to read the bible file:
def read_bible(file_path):
	essential_columns = ['verse_id', 'book_names', 'verse_no_in_chapter', 
	'chapter_id', 'verse_text','read_verse'] 
	try:
		bible_df = pd.read_csv(file_path)
		logging.debug("The file read sucess.")
		if essential_columns not in list(bible_df.columns):
			bible_df = bible_df[['verse_id', 'book_names', 'chapter_id', 
			'verse_no_in_chapter', 'verse_text', 'read_verse']]
			if (
			len(bible_df.read_verse.unique()) == 1
			and bible_df.read_verse.unique()[0] == 1
			):
				bible_df.read_verse = 0
				logging.debug("Reached the end of the bible.")
			return bible_df
		else: 
			raise IndexError(
			"Could not locate the essential columns in the file"
			)
	except Exception as e:
		logging.exception(
		f"Error in initial file read from the path - {file_path}"
		)

# user-defined function to filter the bible file:
def filter_bible(bible_df, verse_to_send):
	bible_df = bible_df[bible_df["read_verse"]==0]
	if bible_df.shape[0] < verse_to_send:
		return bible_df
	else:
		return bible_df.iloc[:verse_to_send]

# user-defined function to create the email content:
def create_email_content(filtered_bible_df):
	subject = ("Bible Sripture " + 
	str(datetime.datetime.now()))
	email_body = ("\nPraise the Lord\n\nToday's Reading:\n\n" + 
	filtered_bible_df.book_names.iloc[0] + " " + 
	filtered_bible_df.chapter_id.astype(str).iloc[0] + ":" + 
	filtered_bible_df.verse_no_in_chapter.astype(str).iloc[0] +
	" - " + filtered_bible_df.book_names.iloc[-1] + " " +
	filtered_bible_df.chapter_id.astype(str).iloc[-1] + ":" +
	filtered_bible_df.verse_no_in_chapter.astype(str).iloc[-1] + 
	"\n\n" + "\n".join(filtered_bible_df.verse_text))
	email_content = {
		"subject":subject,
		"email_body":email_body
	}
	return email_content

# user-defined function to send an email:
def send_email(email_content, receiver_id):
	try:
		server = smtplib.SMTP(host="smtp.office365.com", port=587)
		server.ehlo()
		server.starttls()
		server.login(email_id, password)
		server.sendmail(from_addr=email_id, to_addrs=receiver_id, 
		msg="Subject: {}\n\n{}".format(email_content["subject"], 
		email_content["email_body"]))
		server.quit()
	except Exception as e:
		logging.exception(f"Error in sending the email")

#user-defined function to update the bible file:
def update_bible_file(filtered_bible_df, bible_df):
	bible_df["read_verse"][
	bible_df["verse_id"].isin(filtered_bible_df.verse_id)] = 1
	bible_df.to_csv("/home/pi/Desktop/bible_email_reminder/american_standard_bible.csv", index=False)

if __name__ == "__main__":
	logging.info("Execution begins ")
	bible_df = read_bible(file_path)
	filtered_bible_df = filter_bible(bible_df, verse_to_send)
	email_content = create_email_content(filtered_bible_df)
	for receiver_id in receiver_ids:
		send_email(email_content, receiver_id)
	update_bible_file(filtered_bible_df, bible_df)
	logging.info("Execution sucessfully completed")
