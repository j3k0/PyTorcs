/***************************************************************************

    file                 : simu.cpp
    created              : Sun Mar 19 00:07:53 CET 2000
    copyright            : (C) 2000 by Eric Espie
    email                : torcs@free.fr
    version              : $Id: simu.cpp,v 1.36 2006/02/20 20:15:15 berniw Exp $

 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

#include <stdlib.h>
#include <stdio.h>
#include <memory.h>
#include <math.h>
#ifdef WIN32
#include <windows.h>
#include <float.h>
#define isnan _isnan
#endif

#include "tgf/tgf.h"
#include "sim.h"

tCar *SimCarTable = 0;

tdble SimDeltaTime;

int SimTelemetry;

static int SimNbCars = 0;

t3Dd vectStart[16];
t3Dd vectEnd[16];

#define MEANNB 0
#define MEANW  1


/*
 * Check the input control from robots
 */
static void
ctrlCheck(tCar *car)
{
    tTransmission	*trans = &(car->transmission);
    tClutch		*clutch = &(trans->clutch);

    /* sanity check */
#ifndef WIN32
    if (isnan(car->ctrl->accelCmd) || isinf(car->ctrl->accelCmd)) car->ctrl->accelCmd = 0;
    if (isnan(car->ctrl->brakeCmd) || isinf(car->ctrl->brakeCmd)) car->ctrl->brakeCmd = 0;
    if (isnan(car->ctrl->clutchCmd) || isinf(car->ctrl->clutchCmd)) car->ctrl->clutchCmd = 0;
    if (isnan(car->ctrl->steer) || isinf(car->ctrl->steer)) car->ctrl->steer = 0;
    if (isnan(car->ctrl->gear) || isinf(car->ctrl->gear)) car->ctrl->gear = 0;
#else
    if (isnan(car->ctrl->accelCmd)) car->ctrl->accelCmd = 0;
    if (isnan(car->ctrl->brakeCmd)) car->ctrl->brakeCmd = 0;
    if (isnan(car->ctrl->clutchCmd)) car->ctrl->clutchCmd = 0;
    if (isnan(car->ctrl->steer)) car->ctrl->steer = 0;
    if (isnan(car->ctrl->gear)) car->ctrl->gear = 0;
#endif

    /* check boundaries */
    if (car->ctrl->accelCmd > 1.0) {
	car->ctrl->accelCmd = 1.0;
    } else if (car->ctrl->accelCmd < 0.0) {
	car->ctrl->accelCmd = 0.0;
    }
    if (car->ctrl->brakeCmd > 1.0) {
	car->ctrl->brakeCmd = 1.0;
    } else if (car->ctrl->brakeCmd < 0.0) {
	car->ctrl->brakeCmd = 0.0;
    }
    if (car->ctrl->clutchCmd > 1.0) {
	car->ctrl->clutchCmd = 1.0;
    } else if (car->ctrl->clutchCmd < 0.0) {
	car->ctrl->clutchCmd = 0.0;
    }
    if (car->ctrl->steer > 1.0) {
	car->ctrl->steer = 1.0;
    } else if (car->ctrl->steer < -1.0) {
	car->ctrl->steer = -1.0;
    }

    clutch->transferValue = 1.0 - car->ctrl->clutchCmd;
}

/* Initial configuration */
void
SimConfig(tCarElt *carElt)
{
    tCar *car = &(SimCarTable[carElt->index]);

    memset(car, 0, sizeof(tCar));

    car->carElt = carElt;
    car->DynGCg = car->DynGC = carElt->_DynGC;
    car->ctrl   = &carElt->ctrl;
    car->params = carElt->_carHandle;
    
    SimCarConfig(car);

    sgMakeCoordMat4(carElt->pub.posMat, carElt->_pos_X, carElt->_pos_Y, carElt->_pos_Z - carElt->_statGC_z,
		    RAD2DEG(carElt->_yaw), RAD2DEG(carElt->_roll), RAD2DEG(carElt->_pitch));
}

/* After pit stop */
void
SimReConfig(tCarElt *carElt)
{
    tCar *car = &(SimCarTable[carElt->index]);
    if (carElt->pitcmd.fuel > 0) {
	car->fuel += carElt->pitcmd.fuel;
	if (car->fuel > car->tank) car->fuel = car->tank;
    }
    if (carElt->pitcmd.repair > 0) {
	car->dammage -= carElt->pitcmd.repair;
	if (car->dammage < 0) car->dammage = 0;
    }
}


static void
RemoveCar(tCar *car, tSituation *s)
{
}



void
SimUpdate(tSituation *s, double deltaTime, int telemetry)
{
	int i;
	int ncar;
	tCarElt *carElt;
	tCar *car;
	
	SimDeltaTime = deltaTime;
	SimTelemetry = telemetry;
	for (ncar = 0; ncar < s->_ncars; ncar++) {
		SimCarTable[ncar].collision = 0;
		SimCarTable[ncar].blocked = 0;
	}
	
	for (ncar = 0; ncar < s->_ncars; ncar++) {
		car = &(SimCarTable[ncar]);
		carElt = car->carElt;
	
		if (s->_raceState & RM_RACE_PRESTART) {
			car->ctrl->gear = 0;
		}
	
		CHECK(car);
		ctrlCheck(car);
		CHECK(car);
		SimSteerUpdate(car);
		CHECK(car);
		SimGearboxUpdate(car);
		CHECK(car);
		SimEngineUpdateTq(car);
		CHECK(car);
	
		if (!(s->_raceState & RM_RACE_PRESTART)) {
	
			SimCarUpdateWheelPos(car);
			CHECK(car);
			SimBrakeSystemUpdate(car);
			CHECK(car);
			SimAeroUpdate(car, s);
			CHECK(car);
			for (i = 0; i < 2; i++){
				SimWingUpdate(car, i, s);
			}
			CHECK(car);
			for (i = 0; i < 4; i++){
				SimWheelUpdateRide(car, i);
			}
			CHECK(car);
			for (i = 0; i < 2; i++){
				SimAxleUpdate(car, i);
			}
			CHECK(car);
			for (i = 0; i < 4; i++){
				SimWheelUpdateForce(car, i);
			}
			CHECK(car);
			SimTransmissionUpdate(car);
			CHECK(car);
			SimWheelUpdateRotation(car);
			CHECK(car);
			SimCarUpdate(car, s);
			CHECK(car);
		} else {
			SimEngineUpdateRpm(car, 0.0);
		}
	}
	
	for (ncar = 0; ncar < s->_ncars; ncar++) {
		car = &(SimCarTable[ncar]);
		CHECK(car);
		carElt = car->carElt;
	
		if (carElt->_state & RM_CAR_STATE_NO_SIMU) {
			continue;
		}
	
		CHECK(car);
	
		/* copy back the data to carElt */
	
		carElt->pub.DynGC = car->DynGC;
		carElt->pub.DynGCg = car->DynGCg;
		sgMakeCoordMat4(carElt->pub.posMat, carElt->_pos_X, carElt->_pos_Y, carElt->_pos_Z - carElt->_statGC_z,
				RAD2DEG(carElt->_yaw), RAD2DEG(carElt->_roll), RAD2DEG(carElt->_pitch));
		for (i = 0; i < 4; i++) {
			carElt->priv.wheel[i].relPos = car->wheel[i].relPos;
			carElt->_brakeTemp(i) = car->wheel[i].brake.temp;
			carElt->pub.corner[i] = car->corner[i].pos;
		}
		carElt->_gear = car->transmission.gearbox.gear;
		carElt->_enginerpm = car->engine.rads;
		carElt->_fuel = car->fuel;
		carElt->priv.collision |= car->collision;
		carElt->_dammage = car->dammage;
	}
}


void
SimInit(int nbcars)
{
    SimNbCars = nbcars;
    SimCarTable = (tCar*)calloc(nbcars, sizeof(tCar));
}

void
SimShutdown(void)
{
    tCar *car;
    int	 ncar;

    if (SimCarTable) {
	for (ncar = 0; ncar < SimNbCars; ncar++) {
	    car = &(SimCarTable[ncar]);
	    SimEngineShutdown(car);
	}
	free(SimCarTable);
	SimCarTable = 0;
    }
}

