# Instructions

### How to export your Telegram chat history as a `.json` file:
1. Download and install Telegram Desktop
2. Open Telegram Desktop and click on the chat you wish to export chat history for
3. Click on the icon with 3 dots in the top right corner of the chat
4. Select 'Export chat history'
5. Select 'Format' in 'Chat Export Settings' and change export format from `HTML` to `JSON` **(Important!)**
6. Click 'Save' and then 'Export'
7. Find the `.json` file in your respective folder for downloaded files on your computer

## Detailed Explanation
### 1. Download and install Telegram Desktop
<img width="902" alt="Screenshot 2022-12-25 at 12 47 18" src="https://user-images.githubusercontent.com/106811131/209458902-ea2df5a5-f5d9-4e7c-93f4-634682a2fd6f.png">

If you do not have **Telegram Desktop** installed on your computer, head to the [**official website**](https://desktop.telegram.org) for Telegram Desktop to download the latest version of Telegram Desktop for the appropriate operating system.

### 2. Open Telegram Desktop and click on the chat you wish to export chat history for

### 3. Click on the icon with 3 dots in the top right corner of the chat
![image](https://user-images.githubusercontent.com/106811131/209459070-795d3a8a-843f-4f6c-b4ac-90c5acdb4edd.png)

### 4. Select 'Export chat history'
<img width="391" alt="Screenshot 2022-12-25 at 12 50 07" src="https://user-images.githubusercontent.com/106811131/209459092-fa5c42d6-9ff6-4623-9308-80b13b939584.png">

Upon selecting 'Export chat history', this menu should pop up. You may choose whether to leave the checkboxes ticked or unticked, as the app will not be able to process them. However, the `.json` file will still record these types of files (Photos, videos etc.) as message instances and they will be included in the data.

### 5. Select 'Format' in 'Chat Export Settings' and change export format from `HTML` to `JSON` **(Important!)**
<img width="373" alt="Screenshot 2022-12-25 at 12 50 11" src="https://user-images.githubusercontent.com/106811131/209459186-7f499378-4d85-47ad-ac81-be93fcc1694d.png">

By far the most important step of the process. Ensure that the export format of the file is in `.json` and **NOT** `.html`.

### 6. Click 'Save' and then 'Export'

After this step, you will be able to view the message download progress from your Telegram Desktop interface. Your download may take anywhere from a few seconds to a few days depending on how many messages the chat group has.

### 7. Find the `.json` file in your respective folder for downloaded files on your computer
<img width="656" alt="Screenshot 2022-12-25 at 12 51 04" src="https://user-images.githubusercontent.com/106811131/209459302-7087d565-87a8-4251-bdd1-743acc637a53.png">

Once your download has completed, a pop-up window on Telegram Desktop should appear, indicating that the file has finished downloading. This pop-up-window may contain a button stating 'SHOW MY DATA', which upon clicking sends the user to the file with the downloaded `.json` file.
Congratulations! You have finally learnt to export your Telegram chat data in a `.json` format.

# FAQ:

#### Q: Why does your app only allow `.json`, and not `.html` files to be processed? 
A: There are several major reasons for choosing `.json` files to be used instead of `.html` files for the application. Firstly, parsing data is arguably more difficult and tedious in `.html` format, while `.json` provides data in a more structured and flexible way which is easier for programmers to work with, especially when creating web applications for data. Secondly, `.json` files typically can store a larger amount of data compared to `.html` files. Uploading a 100MB `.json` file to the app is much more convenient than several `.html` files, from both the programmer's and the user's perspective. Lastly, due to how Telegram messages are displayed in `.html` format, there is a high likelihood of information loss during data processin if one were to simply treat the `.html` file as a webpage and use a web scraping library to scrape data from the file.

#### Q: What does `.json` stand for?
A: **JavaScript Object Notation**, or `.json` for short, is an open standard file format, data interchange format and language-independent data format that uses human-readable text to store and transmit data objects consisting of attribute–value pairs and arrays (or other serializable values). Despite first being derived from JavaScript, many modern programming languages include code to generate and parse JSON-format data. JSON filenames use the extension .json. Any valid JSON file is a valid JavaScript (.js) file, even though it makes no changes to a web page on its own.

Source: [**Wikipedia**](<https://en.wikipedia.org/wiki/JSON>)
