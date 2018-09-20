import json
import numpy as np
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

with open('data/detected_objects.json') as json_file:
    objects = json.load(json_file)

with open('data/x.json') as json_file:
    x = json.load(json_file)

with open('data/vehicle_state.json') as json_file:
    vehicleState = json.load(json_file)

with open('data/car_state.json') as json_file:
    carState = json.load(json_file)

tCar = list()
xCar = list()
yCar = list()
for i in carState['car_state']:
    xCar.append(i['pose']['pose']['position']['x'])
    yCar.append(i['pose']['pose']['position']['y'])
    tCar.append(i['time'])

tCmd = list()
speedCmd = list()
for i in x['x']:
    speedCmd.append(i['x'])
    tCmd.append(i['time'])
tCmd = np.array(tCmd)
speedCmd = np.array(speedCmd)

tFb = list()
speedFb = list()
autoMode = list()
for i in vehicleState['vehicle_state']:
    speedFb.append(i['speed'])
    tFb.append(i['time'])
    autoMode.append(i['auto_mode'])
tFb = np.array(tFb)
speedFb = np.array(speedFb)
autoMode = np.array(autoMode)

aaa = tCmd[np.where( speedCmd == 0.0 )]
bbb = speedCmd[np.where( speedCmd == 0.0 )]

tObj = list()
for i in objects['detected_objects']:
    tObj.append(i['time'])
tObj = np.array(tObj)

tSub = list()
for i in objects['detected_objects']:
    tSub.append(abs(i['time']-aaa[0]))
tSub = np.array(tSub)

tCarTime = list()
for i in carState['car_state']:
    tCarTime.append(abs(i['time']-aaa[0]))
tCarTime = np.array(tCarTime)

xCarNow = carState['car_state'][np.argmin(tCarTime, axis=0)]['pose']['pose']['position']['x']
yCarNow = carState['car_state'][np.argmin(tCarTime, axis=0)]['pose']['pose']['position']['y']
thetaCarNow = carState['car_state'][np.argmin(tCarTime, axis=0)]['pose']['pose']['orientation']['z']
c, s = np.cos(thetaCarNow), np.sin(thetaCarNow)

#xObj = list()
#yObj = list()
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

zObj = list()
for i in objects['detected_objects'][np.argmin(tSub, axis=0)]['objects']:
    xObj = list()
    yObj = list()
    for j in i['convex_hull']['polygon']['points']:
        xObj.append(j['x']*c - j['y']*s + xCarNow)
        yObj.append(j['x']*s + j['y']*c + yCarNow)
        zObj.append(j['z'])
    #print ('xObj: {}'.format(xObj))
    #print ('yObj: {}'.format(yObj))
    arr = [[xx,yy] for (xx,yy) in zip(xObj,yObj)]
    #print ('arr: {}'.format(arr))
    pgon = plt.Polygon(arr, alpha=0.5)
    ax.add_patch(pgon)


#xObj = np.array(xObj)
#yObj = np.array(yObj)
zObj = np.array(zObj)

#plt.plot(tCmd, speedCmd)
#plt.plot(aaa, bbb, '.')
# plt.plot(tFb, speedFb)
# plt.plot(tFb, autoMode)
#plt.show()

#fig = plt.figure()
plt.plot(xCar, yCar, '.')
#plt.plot(xObj, yObj, 'o')
plt.plot(xCarNow, yCarNow, 'x', markersize=20)
#ax = fig.add_subplot(111, projection='3d')

#ax.scatter(xObj, yObj, zObj, c='r', marker='.')

#ax.set_xlabel('x axis')
#ax.set_ylabel('y axis')
#ax.set_zlabel('z axis')
plt.show()

