#   Name:       491 - Final Project   
#   Purpose:    Automate the conversion of a feature class (containing images)
#               into a file geodatabase, download the file, and append it to
#               an existing project in the desktop ArcGIS environment
#   Author:     A.J. Thompson   
#   Created:    12/03/2021 


#Import libraries
print("Initializing Libraries")
try:
    import zipfile
    import arcpy
    import arcgis
    from arcgis.gis import GIS
except:
    print("Failed to load libraries, was program run in ArcGIS?")
print("Done")

#set up workspace, this is also where files will be downloaded
workspace = r'C:\Users\GIS Intern\Desktop' nbvc
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

#function for downloading files
def downloadUserItems(owner, downloadFormat):
    try:
        #search for items with the name set earlier
        items = login.content.search(query=web_query, item_type='Feature Service', max_items = 1)
        #loop through them because thats what works
        for item in items:
            #print item id
            print(item)
            print("Downloading Item: " + item.id)
            #try to export the file allowing time for it to finish
            try:
                result = item.export(' {}'.format(item.title), downloadFormat, wait=True)
                time.sleep(10)
                print('Downloaded ' + item.name)

                #download the file in the desired path
                result.download(workspace)
            except Exception as e:
                print(e)      
    except Exception as e:
        print(e)

#login info, "demo" is used for demonstration purposes
#username = input("Enter username(type 'demo' to run automatically): ")
username = demo
if username == "demo":
    #set log in credentials for demo
    login = GIS(None, "Username", "Password",verify_cert=False)
    print("Logged in as Demo User")
    layer_to_download = "Layer to download"
    web_query = 'title:' + layer_to_download
else:
    password = input("Enter password: ")
    #set log in credentials for a real user
    login = GIS(None, username, password,verify_cert=False)
    print("Logged in as Real User")
    layer_to_download = input("Enter name of layer to download")
    web_query = 'title:' + layer_to_download

#call the download function as either demo or user
if username == "demo":
    downloadUserItems('491_Test', 'File Geodatabase')
    print('"Downloading" Files')
    time.sleep(5)
else:
    downloadUserItems(username, 'File Geodatabase')
print("Download Complete")

#unzip the downloaded file
print("Unzipping")
try:
    with zipfile.ZipFile(str(layer_to_download + ".zip"), "r") as zip_ref:
        zip_ref.extractall(workspace)
except Exception as e:
    print(e)
    print("Unable to extract zip file, possibly in the wrong directory")
else:
    print("done")


# This is the code that would be used to update an old layer with the one just downloaded
# however, it wont work for a number of reasons so I choose to comment it out.
#   aprx = arcpy.mp.ArcGISProject(workspace)


#   map = aprx.listMaps("Map")[0]

#   layer = map.listLayers("Layer to update")[0]
#   layer.updateConnectionProperties(current_connection_info=[OldSource], new_connection_info=[NewSource])
