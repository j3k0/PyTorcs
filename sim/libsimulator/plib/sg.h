#ifndef SG_H
#define SG_H  1

#include <float.h>
#include <math.h>

#define SGfloat float
#define SG_ZERO  0.0f
#define SG_ONE   1.0f
#define SG_180   180.0f
#define SG_PI  3.1415926535f
#define SG_DEGREES_TO_RADIANS  (SG_PI/SG_180)
#define SG_RADIANS_TO_DEGREES  (SG_180/SG_PI)

typedef SGfloat sgMat4 [4][4];
void sgMakeCoordMat4(sgMat4 m, const SGfloat x, const SGfloat y, const SGfloat z, const SGfloat h, const SGfloat p, const SGfloat r);

#endif
