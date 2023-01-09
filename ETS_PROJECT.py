import pprint
from graphics import *
import pickle
import sys


def display_menu():
    """
    This function displays the main menu and returns the user's choice
    Parameters: None 
    Returns: menu_choice (string) - the user's input command
    
    """     
     
    print("""
     Edmonton Transit System
---------------------------------
(1) Load shape IDs from GTFS file 
(2) Load shapes from GTFS file 
(3) Load stops from GTFS file

(4) Print shape IDs for a route
(5) Print points for a shape ID
(6) Print stops for a location

(7) Save shapes, shape IDs and stops in a pickle 
(8) Load shapes, shape IDs and stops from a pickle 

(9) Display interactive map 

(0) Quit""")    
    
    menu_choice = input("\nEnter command: ")
    
    while not menu_choice.isdigit() or 0 < int(menu_choice) > 9 :
        menu_choice = input("Enter command: ")       
    
    return menu_choice  
    
#============================================================================

def get_filename(fName):
    '''
    prompts user for a file name, and if nothing is entered, this uses the file
    name fName provided, and returns that prefixed with "data/".; thus, the
    file is expected to be found in folder "data".  NOTE: NO error checking
    '''
    file_name = input("\nEnter a file name [data/trips.txt]: ")
    if file_name == "":
        file_name = "data/" + fName
    
    return file_name

#--------------------------------

def get_filename_shapes(fName):
    '''
    prompts user for a file name, and if nothing is entered, this uses the file
    name fName provided, and returns that prefixed with "data/".; thus, the
    file is expected to be found in folder "data".  NOTE: NO error checking
    '''
    file_name = input("\nEnter a file name [data/shapes.txt]: ")
    if file_name == "":
        file_name = "data/" + fName
    
    return file_name

#----------------------------------

def get_filename_stops(fName):
    '''
    prompts user for a file name, and if nothing is entered, this uses the file
    name fName provided, and returns that prefixed with "data/".; thus, the
    file is expected to be found in folder "data".  NOTE: NO error checking
    '''
    file_name = input("\nEnter a file name [data/stops.txt]: ")
    if file_name == "":
        file_name = "data/" + fName
    
    return file_name
        
#==========================================================================

def get_data(file_name="data/trips.txt"):
    '''
    This expects a file name and returns the file contents in a list 
    of strings corresponding to each line in the file, or None 
    if the file doesn't exist.
    
    '''
        
    try:
        print("opening file...", end = "")
        file = open(file_name, "rt")
    except:
        print(f"\nThere was a problem opening the file {file_name}")
        return None 
    print("reading file...", end = "")
    data = file.readline()      # Skip 1st line
    data = file.readlines()
    print("done reading.")    
    file.close()
    return data


#--------------------------------------------


def get_shapes_coords(file_name = "data/shapes.txt"):
    '''
    This expects a file name,
    shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence
    loads the file contents, skips the first line, and returns a dictionary of
    <key, value> pairs, with key = value before the first comma, and value = 
    a list of 2-tuples consisting of two float values after the first comma.
      
    '''

    try:
        print("opening file...", end = "")
        file = open(file_name, "rt")
    except:
        print(f"\nThere was a problem opening the file {file_name}")
        return None 
    print("reading file...", end = "")
    data = file.readline()        # Skip 1st line
    data = file.readlines()
    print("done reading.")    
    file.close()
    return data
    
    
#========================================================================


def create_routes_dict(data):
    '''
    This expects  data list, which is a list of strings corresponding to each 
    line in the file, It skips the first line, and returns a dictionary of
    <key, value> pairs, with key = value before the first comma, and a 
    list a list of strings consisting of the unique element after the 6th comma
    from every line starting with the same key.
      
    '''
    routes = {}   # to be returned: routes dict shown above
    
    for line in data:
        
        line = line.strip()
        strpd_line = line.split(",")
        route = strpd_line[0]
        shape_ID = strpd_line[-1]
        if route not in routes:
            routes[route] = [shape_ID]
        else:
            if shape_ID not in routes[route]:
                routes[route].append(shape_ID)
        
        
    return routes


#----------------------------------


def create_coords_dict(data):
    '''
   This expects a list of string and return a dictionary that looks like this:
     { '1-30-1'   : [ (53.53864, -113.42325), (53.53863, -113.42329), 
                      (53.5386, -113.42332), ... (53.5206, -113.62288) ]
       ...
       '977-14-1' : [ (53.45622, -113.42523), (53.45623, -113.42524), 
                      (53.45693, -113.42644), ... (53.45786, -113.42803) ] }
   prompts user for 
   '''
    shapes = {}      # to be returned
    
    for line in data:
        
        line = line.strip()
        shape_ID, lat, lon, seq_no = line.split(",")
        if shape_ID not in shapes:
            #routes[route] = [shape_ID]
            shapes[shape_ID] = [(float(lat), float(lon))]
        else:
            if lat not in shapes[shape_ID]:
                shapes[shape_ID].append((float(lat), float(lon)))
        
        
    return shapes

#========================================================================

def display_ShapeIDs(routes):
    '''
    This expects a dictionary structured as follows:
     {'98': ['98-5-1', '98-6-1'],
      '99': ['99-26-1', '99-25-1', '99-8-1', '99-21-1']}
    prompts user for for a route no., ex. 98, and then displays something like:
       ShapeIDs for 98:
	  98-5-1
          98-6-1
    returns : None
    '''
    usr_route = input("Route?: ")
    if usr_route not in routes:
        print(f"Shape IDs for {usr_route}:\n** NOT FOUND **")
    else:
        for item in routes[usr_route]:
            print(item)
    
    return


#------------------------------------------


def display_coords(shapes):
    '''
    This expects a dictionary structured as follows:
     {'98': ['98-5-1', '98-6-1'],
      '99': ['99-26-1', '99-25-1', '99-8-1', '99-21-1']}
    prompts user for for a route no., ex. 98, and then displays something like:
       Shapes for 1-30-1:
	  (53.53864, -113.42325)
          (53.53863, -113.42329)
          (53.5386, -113.42332)
          (53.53856, -113.42333)
          (53.53838, -113.42333)
          (53.53831, -113.42325)
    returns : None

    '''

    usr_shapeID = input("Shape ID?: ")
    if usr_shapeID not in shapes:
        print(f"Shape IDs for {usr_shapeID}:\n** NOT FOUND **")
    else:
        print(f"Shape for {usr_shapeID}:")
        for item in shapes[usr_shapeID]:
            print(item)
    
    return



#=========================================================================



def save_in_pickle(fname_pickle , shapeIDs, shapes, stops):
    '''
    This expects a file name, aswell as the ShapeID dict and shapes dict. It
    then dumps the info in both dicts in a new created file. Then returns that
    file
    '''
   
    
    shapes_n_shapeIDs = (shapeIDs, shapes, stops)
    
    try:
        print("opening file...", end = "")
        fPkle = open(fname_pickle, "wb")
    except:
        print(f"\nThere was a problem opening the file {f_pickle}")
        return None     
    pickle.dump(shapes_n_shapeIDs , fPkle )
    print("dumping to file... done dumping!")
    
    return fPkle
    
  
    
      
  
    
    
    
#----------------------------------------------------



def load_from_pickle(fPkle, f_pickle):
    '''
    This expects a pickeled file, and then loads the info contained in that file
    to a tuple. and returns that tuple. The tuple containes two dicts:
    shapes dict and Shape_IDS dict.
    '''
    try:
        print("opening file...", end = "")
        fPkle = open(f_pickle, "rb")
    except:
        print(f"\nThere was a problem opening the file {f_pickle}")
        return None       
    from_pkle = pickle.load(fPkle)
    print("loading file... done loading!")
     
    
    fPkle.close()
    return from_pkle
    
    
    
#---------------------------------GUI BUSINESS--------------------------------


#=======================================================================


def Edmonton_GUI(from_pkle):
    """
    This menu option uses graphics.py to create a rudimentary graphical user
    interface (GUI). The created window will have an image of edmonton city map.
    When the user enters a bus route number into the text entry box and 
    clicks on the “Plot” rectangle, the program responds.
    If the provided route number does not exist, the button will say
    No Bus {route}. If it exists, it plots the one shape for that bus route that
    contains the most points.
    
    """
    
    shape_ids , shapes, stops = from_pkle
  
    
    win = GraphWin("Edmonton Transit System", 630, 768)
    YEG_image = Image(Point(0,0), "Background.gif")
    w, h = YEG_image.getWidth(), YEG_image.getHeight()
    YEG_image.move(w//2, h//2)
    YEG_image.draw(win)
    
    # Creates a rectangle and centered Text
    r = Rectangle(Point(130,15), Point(240,35))
    r.setFill("white")
    r.draw(win)
    t = Text(r.getCenter(), "Plot")
    t.draw(win)
    
    inputBox = Entry(Point(70, 25), 10) 
    inputBox.setText("747")
    inputBox.setFill("white")
    inputBox.draw(win)
    
 
    win.setCoords(-113.7136, 53.39576, -113.2714, 53.71605)
    
    
    
    while True:     # Main GUI loop
        try:
            geo = win.getMouse()  # Get geographical coords
            lat, lon = geo.y , geo.x
            
            pt = win.toScreen(lon, lat)  # toScreen() returns tuple
            pix = Point(pt[0], pt[1])  # convert tuple to a Point object
            
            
            # Printing out the geo location and closest 5 stops in the terminal
            if not btn_clicked(pix,(r,t)):
                print(f"\nGeographic (lat, lon): ({lat}, {lon})")
                print(f"Pixel (x, y): ({pix.x}, {pix.y})")                
                stops5 = closest_stops(lat, lon, stops, num=5)
                plot_stops(win, stops5)
                print_closest_stops(stops5)
                sys.stdout.flush()                
            
            # Plotting the bus route after user hits the plot button
            if btn_clicked(pix,(r,t)):
                route = inputBox.getText()[:3]
                plot_route(win, shape_ids, shapes, route, t)
        
        # Catching the error when user hit the close button and handling it
        # without crashing the program
        except GraphicsError:    
            win.close()  
            return      
    

    
#========================================================================

def btn_clicked(pt, btn):
    """
    Return True if Point pt is inside the boundaries of button btn
    btn : (Rectangle, Text)
    """
    p1, p2 = btn[0].getP1(), btn[0].getP2()
    return p1.x <= pt.x <= p2.x and p1.y <= pt.y <= p2.y




def plot_route(win, shape_ids, shapes, route, t):
    """
    This plots the specified route, by joining all coordinates in shapes dict,
    using the longest shape in the shape_ids dict.
    returns : None
    
    """  
    
    longest_shape_id = {}
    
    
    if route not in shape_ids:
        t.setText(f"No Bus: {route}")
        t.setFill("red")
    else:
        t.setText(f"Bus: {route}")
        t.setFill("green")
        
        for shape_ID in shape_ids[route]: 
            if len(shape_ID) > len(longest_shape_id):
                longest_shape_id = shape_ID
        
        value = shapes[longest_shape_id]  # values = list of tuples()
        #  Drawing the route
        for i in range(len(value)-1):
            #print(value[(i+1)][0],  value[(i+1)][1])   dev check
            line = Line(Point(value[i][1],  value[i][0]),
                        Point(value[(i+1)][1],value[(i+1)][0] ))
            line.setOutline("gray50")
            line.setWidth(3)
            line.draw(win)
            
    
    
    
#-------------------------------------------------------------------------------
                        # MS3: BUS STOP RELATED
 
    

def load_stops(fName="data/Stops.txt"):
    '''
    This reads bus stop information from file fName
    and returns a dictionary with bus stop (lat, long) as keys, and a list of
    (bus stop ID, bus stop name) tuples for each.
    '''

    try:
        print("opening file...", end = "")
        fIn = open(fName)
    except:
        print(f"\nThere was a problem opening the file {fName}")
        return None
    print("reading file...", end = "")
    lines = fIn.readlines()[1:]          # Skips the first line
    print("done reading.")  
    fIn.close()
    
    stops = {}   # Dict to be returned
    
    for line in lines:
        stuff = line.strip().split(",")
        stop_id, name = stuff[0], stuff[2].strip('""') 
        lat, long = float(stuff[4]), float(stuff[5])
        stops[(lat,long)] = [(stop_id, name )]
   
    
    return stops



def haversine(lat1, lon1, lat2, lon2):
    """
    This function returns great-circle distances between two points on earth
    from their longitudes and latitudes ( (lat1, lon1) and (lat2, lon2) )
    
    From: https://rosettacode.org/wiki/Haversine_formula#Python 
    ------------------------
    Ex. haversine(36.12, -86.67, 33.94, -118.40) = 2887.25995 (km)
    """
    from math import radians, sin, cos, sqrt, asin
     
    #R = 6372.8  # Earth radius in kilometers
    R = 6372800  # Earth radius in meters
    
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
 
    a = sin(dLat / 2)**2 + cos(lat1) * cos(lat2) * sin(dLon / 2)**2
 
    return R * 2 * asin(sqrt(a))    
    

def closest_stops(lat, long, stops, num=5):
    '''
    Given a dictionary of bus stops, ex.
    { (53.571965, -113.390362) : [('1001', 'Abbottsfield Transit Centre')] ... }
    and location (lat, long), this computes the distances from (lat, long) to
    all entries in stops, constructs a list of all these distances, which is 
    then sorted by distance, and returns a list of the first num; ex.: 
       closest_stops(53.57196, -113.3903, stops)
    returns a list of (num) lists [ distance, stop_id, stop_name, lat, long ]: 
    '''

    distances = []
    
    for loc, info in stops.items():
        dist = haversine(lat, long, loc[0], loc[1])
        stop_name = info[0][1].strip('""')
        distances.append([round(dist,1), info[0][0], stop_name, loc[0], loc[1] ])
    
    return sorted(distances)[:num] 

def plot_stops(win, stops):
    '''
    This expects GraphWin, and a list of bus stops
    and plots a Point at each one.
    '''
    for i in range(5):
        aPoint = Point(stops[i][4], stops[i][3]).draw(win)


def print_stops(stops_dict):
    """
    Given a dictionary of bus stops
    this prompts the user for a lat and lon and then prints the stopID and 
    description for that corresponding lon and lat.
    """
    
    usr_loc = input("Location as 'lat, lon'?: ")
    lon, lat = usr_loc.split(",")
    usr_tuple = (float(lon), float(lat))
    
    # Printing the Distance, Stop, and Description of closest 5 stops
    for key, value in stops_dict.items():
        if key == usr_tuple:
            print(f"Stops for ({usr_loc}):\n\t",
                  value[0][0],"\t",value[0][1])
            return
    print(f"Stops for ({usr_loc}):\n"
            "** NOT FOUND ** ")
        

def print_closest_stops(stops):
    '''
    This expects list of the nearest bus stops
    and for each prints out the distance, bus stop id, and name.
    '''

    five_stops = stops[0]
    print(f"""Nearest stops:
      Distance  Stop    Description""")
   
    for item  in range(5):
        #print(f"{stops[item]}")        # Dev Check
        print(f"\t{stops[item][0]}\t{stops[item][1]}\t{stops[item][2]}")
        
    





#=========================================================================



def main():
    """
    This is the main function. It calls helper functions to display a menu, 
    open a file, create a dictionary and display specific ShapeIDs for routes,
    or specific co-ordinates within a shapeID.
    Parameters: None 
    Returns: None
    
    """     
    data = "" # data within in either a shapes or trips file
    routes_dict = {}     # dictionary with routes as keys
    coords_dict = {}     # dictionary with shapes as keys
    from_pkle = () # tuple containing shape_ids and shapes
    
    menu_choice = display_menu()
        
    
    while menu_choice != "0":      
        
        if menu_choice == "1":
            file_name = get_filename("trips.txt") 
            data = get_data(file_name)
            
            if data != None:
                routes_dict = create_routes_dict(data)
                
            #pprint.pprint(data)   #test code: if you want to see the data
            #pprint.pprint(routes_dict)#test code: if you want to see the routes
        
        elif menu_choice == "2":
            file_name = get_filename_shapes("shapes.txt")  
            coords_data = get_shapes_coords(file_name)
            #pprint.pprint(coords_data) #Test code to see the structure of
                                        #co-ords data

            if coords_data != None:
                coords_dict = create_coords_dict(coords_data)
                #pprint.pprint(coords_dict)  # test code to make sure the
                                     # co-ordinates data is structures properly
        
        elif menu_choice == "3":
            file_name = get_filename_stops("stops.txt")  
            
            stops_dict = load_stops(file_name)
            #pprint.pprint(stops_dict)
        
        elif menu_choice == "4":
            display_ShapeIDs(routes_dict) 
        
        elif menu_choice == "5":
            display_coords(coords_dict) 
        
        elif menu_choice == "6":
            print_stops(stops_dict)         
            
        elif menu_choice == "7":
            f_pickle = input("\nEnter a file name [etsdata.pkl]: ")
            if f_pickle == "":     
                f_pickle = "etsdata.pkl" # choose this file name if input = ""
        
            fPkle = save_in_pickle(f_pickle, routes_dict, coords_dict,\
                                   stops_dict)
        
        elif menu_choice == "8":
            f_pickle = input("\nEnter a file name [etsdata.pkl]: ")
            if f_pickle == "":
                f_pickle = "etsdata.pkl" # choose this file name if input = ""
                
            from_pkle = load_from_pickle(fPkle, f_pickle)
        
        elif menu_choice == "9":
            if len(from_pkle) > 1:            
                Edmonton_GUI(from_pkle)        
    
        menu_choice = display_menu() 
    
    if menu_choice == "0":
        print("Have a good summer break!!!") 
        return    
    
   
   
    
if __name__ == "__main__":
    #Test Code
    main() 
