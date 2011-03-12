/***************************************************************************

    file                 : collide.cpp
    created              : Sun Mar 19 00:06:19 CET 2000
    copyright            : (C) 2000-2005 by Eric Espie, Bernhard Wymann
    email                : torcs@free.fr
    version              : $Id: collide.cpp,v 1.32 2006/02/20 20:15:15 berniw Exp $

 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

#include "sim.h"

#define CAR_DAMMAGE	0.1

void SimCarCollideZ(tCar *car)
{
	int i;
	t3Dd normal;
	tdble dotProd;
	tWheel *wheel;
	const float CRASH_THRESHOLD = -5.0f;

	if (car->carElt->_state & RM_CAR_STATE_NO_SIMU) 
	    {
		return;
	    }

	for (i = 0; i < 4; i++) 
	    {
		wheel = &(car->wheel[i]);
		tWheelState *wheelState = &(car->carElt->priv.wheel[i]);
		if (wheel->state & SIM_SUSP_COMP) 
		    {
			car->DynGCg.pos.z += wheel->susp.spring.packers - wheel->rideHeight;
			
			normal.x =  wheelState->nnorm_x;
			normal.y =  wheelState->nnorm_y;
			normal.z =  wheelState->nnorm_z;
			
			normal.x = 0.0f;
			normal.y = 0.0f;
			normal.z = 1.0f;

			float kRebound = 0.5000f;
			float kDammage = 0.0000f;
			
			dotProd = (car->DynGCg.vel.x * normal.x + car->DynGCg.vel.y * normal.y + car->DynGCg.vel.z * normal.z) * kRebound;
			if (dotProd < 0) 
			    {
				if (dotProd < CRASH_THRESHOLD) 
				    {
					car->collision |= SEM_COLLISION_Z_CRASH;
				    }
				car->collision |= SEM_COLLISION | SEM_COLLISION_Z;
				car->DynGCg.vel.x -= normal.x * dotProd;
				car->DynGCg.vel.y -= normal.y * dotProd;
				car->DynGCg.vel.z -= normal.z * dotProd;
				if ((car->carElt->_state & RM_CAR_STATE_FINISH) == 0) 
				    {
					car->dammage += (int)(kDammage * fabs(dotProd) * simDammageFactor[car->carElt->_skillLevel]);
				    }
			    }
		    }
	    }
}

