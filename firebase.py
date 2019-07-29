# import time
from datetime import date
from firebase import firebase
import mplleaflet
import geopandas as gpd

# use either current data or a specific dates that has data points
# current_date=date.today()

# read the data points from the saved longitude and latitute that is generated by the phone app and written to
# firebase on the cloud from the app in the phone
current_date='2019-07-04'

# get the database to use and read the data into results
firebase=firebase.FirebaseApplication ('https://ionic2do-ee1d2.firebaseio.com',None)
results=firebase.get("/location_"+str(current_date),None)

# every items have a time field. Sort it base on time
z=results.items()
z.sort(key=lambda x: (x[1]['time']))

#this template will draw a line
template_line = \
    ''' \
    { "type" : "Feature",
        "geometry" : {
            "type" : "LineString",
            "coordinates" : [[%s, %s],[%s,%s]]},
        "properties" : {}
        },
    '''        

#this template will draw a point
template_marker = \
    ''' \
    { "type" : "Feature",
        "geometry" : {
            "type" : "Point",
            "coordinates" : [%s, %s]},
        "properties" : {}
        },
    '''
    
# the head of the geojson file
output = \
    ''' \
{ "type" : "FeatureCollection",
    "features" : [
    '''

# this routine will write out the geojson file to be plotted out by geopandas
i=0
for uid,items in z: 
    i+=1
    print uid, items.get('time'),items.get('lng'),items.get('lat')
    output += template_marker % (items.get('lng'), items.get('lat'))
    try:
        output += template_line % (items.get('lng'), items.get('lat'),z[i][1].get('lng'), z[i][1].get('lat'))
    except:
        print ("reach end of data points")
    
# the tail of the geojson file
output += \
    ''' \
    ]
}
    '''
    
outFileHandle = open(str(current_date)+".geojson", "w")
outFileHandle.write(output)
outFileHandle.close()

#use the transform data from the saved files and try plotting it 
track=gpd.GeoDataFrame.from_file('./'+ str(current_date)+'.geojson')
# the full path is as per below if the absolute path does not work
# track=gpd.GeoDataFrame.from_file('/Users/mac/projects/python/pydot/'+ str(current_date)+'.geojson')
tr=track.geometry.plot(color='red')

#mplleaflet will show output in map form for easy human readability.
mplleaflet.show(fig=tr.figure)