import os
import sys
import glob
import pickle
import serial
import matplotlib.pyplot as plt

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from sklearn.model_selection import train_test_split
from sklearn.cross_decomposition import PLSRegression

# Import the resources file
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import resources


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Constants
        self.OS_LINUX = 'linux'
        self.OS_WINDOWS = 'windows'
        self.OS_MACOS = 'macos'

        # Operating system
        if sys.platform == 'linux':
            self.os = self.OS_LINUX
        elif sys.platform == 'win32':
            self.os = self.OS_WINDOWS
        elif sys.platform == 'darwin':
            self.os = self.OS_MACOS

        # Load the UI file
        uic.loadUi('gui.ui', self)

        # Update the datapoint counts
        self.updateDatapointCounts()

        if self.os == self.OS_LINUX:
            self.serial = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

        # Button Actions
        # =============== pgSplash ===============
        self.btnSplashStart.clicked.connect(self.fcnSplashStart)
        self.btnSplashTrain.clicked.connect(self.fcnSplashTrain)
        self.btnSplashShutdown.clicked.connect(self.fcnSplashShutdown)

        # =============== pgTrain ===============
        self.btnTrainNewCupcake.clicked.connect(self.fcnTrainNewCupcake)
        self.btnTrainNewDoughnut.clicked.connect(self.fcnTrainNewDoughnut)
        self.btnTrainNewCookie.clicked.connect(self.fcnTrainNewCookie)

        self.btnTrainDeleteCupcake.clicked.connect(lambda: self.deleteDatapoints('cupcake'))
        self.btnTrainDeleteDoughnut.clicked.connect(lambda: self.deleteDatapoints('doughnut'))
        self.btnTrainDeleteCookie.clicked.connect(lambda: self.deleteDatapoints('cookie'))

        self.btnTrainTrainModelCupcake.clicked.connect(lambda: self.fcnTrainModel('cupcake'))
        self.btnTrainTrainModelDoughnut.clicked.connect(lambda: self.fcnTrainModel('doughnut'))
        self.btnTrainTrainModelCookie.clicked.connect(lambda: self.fcnTrainModel('cookie'))

        self.btnTrainExit.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pgSplash))


        # =============== pgChoosePastry ===============
        self.btnChoosePastryBack.clicked.connect(self.fcnChoosePastryBack)
        self.btnChoosePastryCupcake.clicked.connect(self.fcnChoosePastryCupcake)
        self.btnChoosePastryDoughnut.clicked.connect(self.fcnChoosePastryDoughnut)
        self.btnChoosePastryCookie.clicked.connect(self.fcnChoosePastryCookie)


        # =============== pgChoose ===============
        self.btnChooseMen.clicked.connect(self.fcnChooseMen)
        self.btnChooseWomen.clicked.connect(self.fcnChooseWomen)
        self.btnChooseChildren.clicked.connect(self.fcnChooseChildren)
        self.btnChooseBack.clicked.connect(self.fcnChooseBack)
        self.btnChooseProceed.clicked.connect(self.fcnChooseProceed)


        # =============== pgGreen ===============
        self.btnGreenBack.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pgChoose))
        self.btnGreenOk.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pgSplash))

        # =============== pgYellow ===============
        self.btnYellowBack.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pgChoose))
        self.btnYellowOk.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pgSplash))
                                         
        # =============== pgRed ===============
        self.btnRedBack.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pgChoose))
        self.btnRedOk.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pgSplash))




    def fcnChoosePastryBack(self):
        self.stackedWidget.setCurrentWidget(self.pgSplash)
    
    def fcnChoosePastryCupcake(self):
        self.selectedPastry = 'cupcake'
        self.stackedWidget.setCurrentWidget(self.pgChoose)
    
    def fcnChoosePastryDoughnut(self):
        self.selectedPastry = 'doughnut'
        self.stackedWidget.setCurrentWidget(self.pgChoose)
    
    def fcnChoosePastryCookie(self):
        self.selectedPastry = 'cookie'
        self.stackedWidget.setCurrentWidget(self.pgChoose)


    def fcnSplashShutdown(self):
        # Confirm
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Are you sure you want to shutdown the system?")
        msg.setWindowTitle("Shutdown")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        response = msg.exec_()
        if response != QMessageBox.Yes:
            return
        
        # Shut down
        if self.os == self.OS_LINUX:
            os.system('sudo shutdown now')
        else:
            print("Shutting down...")


    def fcnTrainModel(self, pastryType):

        # Check if there is at least 10 data points
        dataPoints = glob.glob(f'../../datasets/{pastryType}/*.txt')
        if len(dataPoints) < 10:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Please collect at least 10 data points for training.")
            msg.setWindowTitle("Error")
            msg.exec_()
            return

        # Confirm
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("This will override any existing model. Are you sure you want to proceed?")
        msg.setWindowTitle("Train Model")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        response = msg.exec_()
        if response != QMessageBox.Yes:
            return
        

        # Compile X and y
        X = []
        y = []
        for data in dataPoints:
            with open(data) as f:
                lines = f.readlines()
            
            y1 = float(lines[0])
            X1 = lines[1].split(',')

            X.append(X1)
            y.append(y1)

        print("Setting aside official testing data...")
        X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.25)

        print("Pre-Splitting Data Count: " , len(X))
        print("Official Test Dataset Count: " , len(X_test))
        print("Training Dataset Count: " , len(X_train))
        

        clf = PLSRegression()
        clf.fit(X_train,y_train)

        # Scores
        trainingScore = clf.score(X_train,y_train)
        testingScore = clf.score(X_test,y_test)

        # Test on the training set
        print("Training Score: " , trainingScore)

        # Test on the test set
        print("Testing Score: " , testingScore)

        # Save the model
        os.makedirs('../../models/', exist_ok=True)

        with open(f'../../models/{pastryType}.pkl', 'wb') as f:
            pickle.dump(clf, f)


        # Visualize with Scatter Plot between Actual and Predicted - Training Data
        y_pred = clf.predict(X_train)

        print(y_train)
        print(y_pred)

        plt.figure(num="Training Data")  # Create a new figure
        plt.scatter(y_train, y_pred)

        # Also plot the line y=x, red broken line
        plt.plot([min(y_train), max(y_train)], [min(y_train), max(y_train)], color='red', linestyle='--')

        plt.xlabel('Actual')
        plt.ylabel('Predicted')
        plt.title('Actual vs Predicted - Training Data')
        plt.legend(['Actual vs Predicted', 'Perfect Prediction Line'])
        plt.show(block=False)



        # Visualize with Scatter Plot between Actual and Predicted - Testing Data
        y_pred = clf.predict(X_test)

        print(y_test)
        print(y_pred)

        plt.figure(num="Testing Data")  # Create a new figure
        plt.scatter(y_test, y_pred)

        # Also plot the line y=x, red broken line
        plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')

        plt.xlabel('Actual')
        plt.ylabel('Predicted')
        plt.title('Actual vs Predicted - Testing Data')
        plt.legend(['Actual vs Predicted', 'Perfect Prediction Line'])
        plt.show()
        
        

        
        # Show success
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Model trained successfully.\n\nTraining Score: {0}\nTesting Score: {1}".format(
            trainingScore,
            testingScore
        ))
        msg.setWindowTitle("Success")
        msg.exec_()



    def fcnTrainNewCupcake(self):
        self.fcnTrainNewData('cupcake')

    def fcnTrainNewDoughnut(self):
        self.fcnTrainNewData('doughnut')

    def fcnTrainNewCookie(self):
        self.fcnTrainNewData('cookie')

    def updateDatapointCounts(self):
        os.makedirs('../../datasets/', exist_ok=True)
        os.makedirs('../../datasets/cupcake', exist_ok=True)
        os.makedirs('../../datasets/doughnut', exist_ok=True)
        os.makedirs('../../datasets/cookie', exist_ok=True)

        cupcakeCounts = glob.glob('../../datasets/cupcake/*.txt')
        doughnutCounts = glob.glob('../../datasets/doughnut/*.txt')
        cookieCounts = glob.glob('../../datasets/cookie/*.txt')

        self.lblTrainCupcakePoints.setText(str(len(cupcakeCounts)))
        self.lblTrainDoughnutPoints.setText(str(len(doughnutCounts)))
        self.lblTrainCookiePoints.setText(str(len(cookieCounts)))


    def fcnTrainNewData(self, pastryType):
        # Send the command to the arduino
        print("Reading data...")
        if self.os == self.OS_LINUX:
            self.serial.write(b'triad\n')
            while True:
                if self.serial.in_waiting > 0:
                    break
        
            # Read string until newline
            data = self.serial.readline().decode('utf-8').strip()
        else:
            # Use dummy data
            data = '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18'

        # Save the data to a file
        print("looking for file...")
        ctr = 0
        while True:
            if os.path.exists(os.path.join('../../datasets', pastryType, f'{ctr}.txt')):
                ctr += 1
                continue
            break
        
        if pastryType == 'cupcake':
            inputVal = self.inputTrainSugarLevelCupcake.text()
        elif pastryType == 'doughnut':
            inputVal = self.inputTrainSugarLevelDoughnut.text()
        elif pastryType == 'cookie':
            inputVal = self.inputTrainSugarLevelCookie.text()

        # Validation
        if inputVal == '':
            # Show qt dialog
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Please enter a sugar level.")
            msg.setWindowTitle("Error")
            msg.exec_()
            return

        # Accept only valid number
        try:
            inputVal = float(inputVal)
        except:
            # Show qt dialog
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Please enter a valid number.")
            msg.setWindowTitle("Error")
            msg.exec_()
            return

        print("saving data...")
        with open(os.path.join('../../datasets', pastryType, f'{ctr}.txt'), 'w') as f:
            f.writelines([
                str(inputVal), '\n',
                data
            ])
        
        # Update the datapoint counts
        self.updateDatapointCounts()

        # Clear the input field
        if pastryType == 'cupcake':
            self.inputTrainSugarLevelCupcake.setText('')
        elif pastryType == 'doughnut':
            self.inputTrainSugarLevelDoughnut.setText('')
        elif pastryType == 'cookie':
            self.inputTrainSugarLevelCookie.setText('')
    
        # Show success
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Data saved successfully.")
        msg.setWindowTitle("Success")
        msg.exec_()
        


    def deleteDatapoints(self, pastryType):
        # Show question dialog
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Are you sure you want to delete all the {0} data points?".format(pastryType))
        msg.setWindowTitle("Delete Data Points")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        response = msg.exec_()
        if response != QMessageBox.Yes:
            return

        # Delete all the files in the directory
        for file in glob.glob(f'../../datasets/{pastryType}/*.txt'):
            os.remove(file)

        # Update the datapoint counts
        self.updateDatapointCounts()

        # Show success
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Data deleted successfully.")
        msg.setWindowTitle("Success")
        msg.exec_()



    def fcnSplashTrain(self):
        self.stackedWidget.setCurrentWidget(self.pgTrain)

    def fcnChooseProceed(self):
        if "selectedRole" not in dir(self):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Please select a role.")
            msg.setWindowTitle("Error")
            msg.exec_()
            return
        
        self.fcnChoosePerformClassification()
    

    def fcnChoosePerformClassification(self):
        # Check if a role has been selected
        if self.selectedRole == None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Please select a role.")
            msg.setWindowTitle("Error")
            msg.exec_()
            return
        
        # Read from serial
        if self.os == self.OS_LINUX:
            self.serial.write(b'triad\n')
            while True:
                if self.serial.in_waiting > 0:
                    break
        
            # Read string until newline
            data = self.serial.readline().decode('utf-8').strip()
        else:
            # Use dummy data
            data = '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18'
        
        # Convert the data to a list of floats
        data = data.split(',')
        data = [float(x) for x in data]
        
        # Classify the reading
        # Load the model
        with open(f'../../models/{self.selectedPastry}.pkl', 'rb') as f:
            clf = pickle.load(f)
        
        sugarLevel = clf.predict([data])[0]

        if sugarLevel < 0:
            sugarLevel = 0

        if self.selectedRole == 'men':
            maxSugar = 37.5
        elif self.selectedRole == 'women':
            maxSugar = 25
        elif self.selectedRole == 'children':
            maxSugar = 20
        
        pctSugar = (sugarLevel / maxSugar) * 100

        if pctSugar > 100:
            pctSugar = 100
        
        if pctSugar <= 40:
            pctLevel = 'green'
        elif pctSugar <= 70:
            pctLevel = 'yellow'
        else:
            pctLevel = 'red'

        
        if pctLevel == 'green':
            self.lblGreenGrams.setText(f'{sugarLevel:.2f} grams')
            self.lblGreenPct.setText(f'{pctSugar:.2f} %')
            self.lblGreenInfo.setText(f'The results are normal and appropriate for health-conscious {self.selectedRole}, with a {pctSugar:.2f} % sweetness level and {sugarLevel:.2f} grams of sugar.')
            
            if self.os == self.OS_LINUX:
                self.serial.write(b'ledGreen\n')
            
            self.stackedWidget.setCurrentWidget(self.pgGreen)
        elif pctLevel == 'yellow':
            self.lblYellowGrams.setText(f'{sugarLevel:.2f} grams')
            self.lblYellowPct.setText(f'{pctSugar:.2f} %')
            self.lblYellowInfo.setText(f'The results are mild. Please be conscious of eating too much sweets for health-conscious {self.selectedRole}, with a {pctSugar:.2f} % sweetness level and {sugarLevel:.2f} grams of sugar.')
            if self.os == self.OS_LINUX:
                self.serial.write(b'ledYellow\n')
            
            self.stackedWidget.setCurrentWidget(self.pgYellow)
        elif pctLevel == 'red':
            self.lblRedGrams.setText(f'{sugarLevel:.2f} grams')
            self.lblRedPct.setText(f'{pctSugar:.2f} %')
            self.lblRedInfo.setText(f'The results are high and not recommended for health-conscious {self.selectedRole}, with a {pctSugar:.2f} % sweetness level and {sugarLevel:.2f} grams of sugar. Please be careful of eating too much sweets and sugar.')
            
            if self.os == self.OS_LINUX:
                self.serial.write(b'ledRed\n')
            
            self.stackedWidget.setCurrentWidget(self.pgRed)

        
    
    def fcnChooseBack(self):
        self.stackedWidget.setCurrentWidget(self.pgChoosePastry)

    def fcnChooseChildren(self):
        # Set the background of this button to green
        self.btnChooseChildren.setStyleSheet("background-color: #0d6d6e")
        # Set the background of the other buttons to unset
        self.btnChooseMen.setStyleSheet("")
        self.btnChooseWomen.setStyleSheet("")
        self.selectedRole = "children"

    def fcnChooseWomen(self):
        # Set the background of this button to green
        self.btnChooseWomen.setStyleSheet("background-color: #0d6d6e")
        # Set the background of the other buttons to unset
        self.btnChooseMen.setStyleSheet("")
        self.btnChooseChildren.setStyleSheet("")
        self.selectedRole = "women"

    def fcnChooseMen(self):
        # Set the background of this button to green
        self.btnChooseMen.setStyleSheet("background-color: #0d6d6e")
        # Set the background of the other buttons to unset
        self.btnChooseWomen.setStyleSheet("")
        self.btnChooseChildren.setStyleSheet("")
        self.selectedRole = "men"


    def fcnSplashStart(self):
        # Go to pgChoose
        self.stackedWidget.setCurrentWidget(self.pgChoosePastry)
        


app = QApplication([])
window = MainWindow()
if window.os == window.OS_LINUX:
    window.showFullScreen()
else:
    window.show()
app.exec_()
    