----

[[_TOC_]]

----

# Car Data Logger Software Installation

*NOTE: These steps assume that you have completed the Car Data Logger installation as documented in the* `Hardware` *folder.  You will need:
- The Certificate file that was generated when you registered the device
- Your AWS IoT Endpoint
- WiFi SSID and Password*

1. Download the `nano_rp2040_iot` folder to your PC and move it to the Arduino sketches home folder.  On a Windows PC this will typically be in `C:\Users\<UID>\Documents\Arduino`.
2. Open the Arduino IDE and then open the nano_rp2040_iot.ino file.  you should see two tabs appear, one for the ino file itself and one for the arduino_secrets.h file.
3. Update the following items in your arduino_secrets.h file:
- SECRET_SIDD: The SIDD of your WiFi network
- SECRET_PASS: The Password for your WiFi network
- SECRET_BROKER: The AWS IoT Endpoint
- SECRET_CERTIFICATE: The *PUBLIC* certificate you got when you registered the device.  *Note: The secret key is stored on your Arduino in the secure element.*
4. Click on the Upload button in the Arduino IDE to compile and upload the sketch.  
5. After the sketch has uploaded and installed on the Arduino nano, open the *Tools > Serial Monitor*.  You should see the device booting up, attaching to the WiFi network and starting the transmission of data.  If you move the Arduino around you will see the accellerometer and gyro recording the movement.

## Integrating with AWS IoT Core

1. Open the AWS Console and navigate to *AWS IoT Core > MQTT Test Client*.  Click on the *Subscripbe to a topic* tab and enter *carid6/gforce* for the *Topic filter* feild.  You should see the data arriving in IoT Core from the Arduino in JSON format.

## Integrating with AWS IoT Core Analytics

1. Open the AWS Console and navigate to *AWS IoT Analytics*.
2. In the *Getting Started* section, type *Scalextric* in the *Resources Prefix* field.  Type *carid6/gforce* in the MQTT Topic field.  Click on the *Create resources* button.  AWS IoT Analytics will now create:
- channel: links IoT Core and IoT Analytics
- pipeline: links the ingest, process and store operations for your data
- rule: copies messages recieved in the topic to the channel.
- datastore: a managed S3 data bucket
- dataset: a view of the data in the store that you can query with SQL
- rule: copies the messages from IoT Core to the target channel in IoT Analytics
3. Your data can now be queried direct from the dataset using Quicksight or Jupyter notebooks.

## Creating Visualisations - Jupyter

1. Open the AWS Console and navigate to *AWS IoT Analytics* > Notebooks*.
2. Click on the *Create Notebook* button.  
3. Click on the *IoTA blank Template* option box and then click on the *next* button.
4. Put a value in for the *notebook name* and select the dataset you created earlier.  Select the *create instance* buttin and fill in the details for a new instance.  you will also need to create a new role as directed.  When you have all the data complete, click on the next button to start creating the notebook.
5. Your notebook instance will not be created.  Click on the instance to start it.  Click on the "open Jupyter" button to start the Jupyter console.
6. You will now see the Jupyter console.  Open the IoTAnalytics folder and then open the <notebook_name>.ipynb file.  You will see that the basic data imorts have already been created for you.
7. Create a new code cell that displays the url of the dataset.
```
dataset_url
```
8. Create a new dataframe and priunt it out so we can see what we have
```
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv(dataset_url, header=0, parse_dates=['time'])
df
```

10. Create a new dataframe using the timestamp as the index to make it queryable
```
datetime_series = pd.to_datetime(df['time'])
datetime_index = pd.DatetimeIndex(datetime_series.values)
df2 = df.set_index(datetime_index)
df2.drop('time', axis=1, inplace=True)
df2.drop('__dt', axis=1, inplace=True)
df2.sort_index(inplace=True)
df2
```
11.  Now you can query between different time slices to see the particular events you are interested in.  Try a query like the one below:
```
df2.between_time('14:44','14:54')
```
12. You can use the new dataframe to create visualisations.  See this example below:
```
df2.plot(subplots=True, figsize=(12,12))
```

13. You can also slice the data up into small timeframes foe example:
```
df3 = df2.between_time('14:44','15:54')
df3
df3.plot(subplots=True, figsize=(12,12))

```
14. Lastly, you can export the data for analytics elsewhere if you like
```
df3.to_csv('gyro.csv', index=True, header=True)
```
