/***************************************************************************

    file                 : raceman.h
    created              : Sun Jan 30 22:59:17 CET 2000
    copyright            : (C) 2000,2002 by Eric Espie
    email                : torcs@free.fr
    version              : $Id: raceman.h,v 1.28 2006/02/20 20:17:43 berniw Exp $

 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 
/** @file
    		This is the race information structures.
    @author	<a href=mailto:torcs@free.fr>Eric Espie</a>
    @version	$Id: raceman.h,v 1.28 2006/02/20 20:17:43 berniw Exp $
    @ingroup	raceinfo
*/
 
#ifndef _RACEMANV1_H_
#define _RACEMANV1_H_

#include "tgf/tgf.h"
#include "interfaces/car.h"
#include "interfaces/simu.h"
#include <stdint.h>

#define RM_RACE_RUNNING		0X00000001 /* Race states */
#define RM_RACE_FINISHING	0X00000002
#define RM_RACE_ENDED		0X00000004
#define RM_RACE_STARTING	0X00000008
#define RM_RACE_PRESTART	0X00000010
#define RM_RACE_PAUSED		0X40000000

/** General info on current race */
typedef struct {
    int32_t	ncars;		/**< number of cars */
    int32_t	state;
} tRaceAdmInfo;

#define _ncars		raceInfo.ncars
#define _raceState	raceInfo.state

/** cars situation used to inform the GUI and the drivers */
typedef struct Situation {
    tRaceAdmInfo	raceInfo;
    double		    deltaTime;
    double		    currentTime;	/**< current time in sec since the beginning of the simulation */
    int32_t		    nbPlayers;	/**< number of human player in local (splitted screen) */
    tCarElt         **cars;		/**< list of cars */ 
} tSituation;

#endif /* _RACEMANV1_H_ */ 
