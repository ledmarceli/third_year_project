1. You must have python installed on your machine. Ideally 3.10.10 or newer. If you don’t have it installed, you can download it for free from this website: https://www.python.org/downloads
2. Go to server/analyse.py and change line 11 to your path to lc0
3. There are also several python modules that you need for this program. They include:
pandas
numpy
torch
chess
These can be installed in your command line by typing:
pip install ‘name of the module’
4. You must have Node.js installed on your machine. Ideally 16.14.2 or newer.
Once you have it installed, find the app.js file in the source. In its directory run the following commands
npm install node
npm install express
npm install cors
npm install path
npm install multer
node app.js 
This should start the local server in your terminal. You don’t have to do anything more at this point. Just type Ctrl+c in your terminal once you want to deactivate it. Next time you want to run it, just navigate to the project directory and type the following command 
node app.js    
5. Once your local server is running just open the main_menu.html file and use the application.
